import ast
from pathlib import Path
from typing import Dict, List, Set

from .config import AnalyzerConfig
from .result import AnalysisResult, UnreachableCode


class CodeAnalyzer:
    def __init__(self, config: AnalyzerConfig):
        self.config = config
        self.result = AnalysisResult()
        self.visited_nodes: Set[ast.AST] = set()
        self.call_graph: Dict[str, Set[str]] = {}
        self.defined_functions: Dict[str, ast.FunctionDef] = {}
        self.reachable_functions: Set[str] = set()
        self.class_instances: Dict[str, List[str]] = {}  # Add this line

    def analyze(self, project_path: str, entry_point: str = None) -> AnalysisResult:
        project_path = Path(project_path)

        if project_path.is_dir():
            python_files = list(project_path.rglob("*.py"))
        elif project_path.is_file():
            python_files = [project_path]
        else:
            raise ValueError(f"Invalid project path: {project_path}")

        # Build initial AST and symbol table
        for file_path in python_files:
            if self._should_analyze_file(file_path):
                with open(file_path) as f:
                    tree = ast.parse(f.read())
                    self._analyze_module(tree, file_path)

        entry_func = entry_point or "main"
        self._trace_reachability(entry_func)

        self._find_unreachable_code()
        return self.result

    def _should_analyze_file(self, file_path: Path) -> bool:
        relative_path = str(file_path)
        return not any(
            pattern.match(relative_path) for pattern in self.config.exclude_patterns
        )

    def _analyze_module(self, tree: ast.AST, file_path: Path):
        """Traverse the AST to collect function definitions and calls."""

        class FunctionCollector(ast.NodeVisitor):
            def __init__(self, analyzer: "CodeAnalyzer"):
                self.analyzer = analyzer
                self.current_class = None

            def visit_FunctionDef(self, node: ast.FunctionDef):
                if self.current_class:
                    func_name = f"{self.current_class}.{node.name}"
                else:
                    func_name = node.name
                self.analyzer.defined_functions[func_name] = node
                self.generic_visit(node)

            def visit_ClassDef(self, node: ast.ClassDef):
                self.current_class = node.name
                self.generic_visit(node)
                self.current_class = None

            def visit_Assign(self, node: ast.Assign):
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        class_name = node.value.func.id
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                instance_name = target.id
                                self.analyzer.class_instances.setdefault(
                                    instance_name, []
                                ).append(class_name)
                self.generic_visit(node)

        collector = FunctionCollector(self)
        collector.visit(tree)

    def _trace_reachability(self, func_name: str):
        """Determine which functions are reachable starting from the entry point."""
        worklist = [func_name]
        reachable = set()

        while worklist:
            current_func = worklist.pop()
            if current_func in reachable:
                continue
            reachable.add(current_func)

            func_def = self.defined_functions.get(current_func)
            if not func_def:
                continue

            for node in ast.walk(func_def):
                if isinstance(node, ast.Call):
                    callee_name = self._get_callee_name(node)
                    if callee_name:
                        # Check if it's a defined function here instead
                        if callee_name in self.defined_functions:
                            worklist.append(callee_name)

        self.reachable_functions = reachable

    def _get_callee_name(self, node: ast.Call) -> str:
        """Extract the callee's name from a Call node."""
        name = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            if isinstance(node.func.value, ast.Name):
                # Instance method call: obj.method()
                instance_name = node.func.value.id
                if instance_name in self.class_instances:
                    class_name = self.class_instances[instance_name][0]
                    qualified_name = f"{class_name}.{method_name}"
                    # Only use qualified name if the method exists
                    name = (
                        qualified_name
                        if qualified_name in self.defined_functions
                        else method_name
                    )
                else:
                    name = method_name
            elif isinstance(node.func.value, ast.Call):
                # Handle cases like ClassName().method()
                if isinstance(node.func.value.func, ast.Name):
                    class_name = node.func.value.func.id
                    qualified_name = f"{class_name}.{method_name}"
                    # Only use qualified name if the method exists
                    name = (
                        qualified_name
                        if qualified_name in self.defined_functions
                        else method_name
                    )
                else:
                    name = method_name
            else:
                name = method_name
        return name

    def _find_unreachable_code(self):
        """Identify functions that are not in reachable functions set."""
        for func_name, func_def in self.defined_functions.items():
            if func_name not in self.reachable_functions:
                code_type = "method" if "." in func_name else "function"
                item = UnreachableCode(
                    file_path=str(func_def.lineno),
                    line_start=func_def.lineno,
                    line_end=getattr(func_def, "end_lineno", func_def.lineno),
                    code_type=code_type,
                    name=func_name,
                    confidence=1.0,
                )
                self.result.add_item(item)
