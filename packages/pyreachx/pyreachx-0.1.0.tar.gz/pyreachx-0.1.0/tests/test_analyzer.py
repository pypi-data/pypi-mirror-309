import ast

import pytest

from pyreachx.analyzer import AnalysisResult, CodeAnalyzer
from pyreachx.config import AnalyzerConfig


def test_analyze_simple_function(tmp_path):
    code = """
def used_function():
    return 42

def unused_function():
    return 24

def main():
    return used_function()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)
    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(file_path), "main")

    unreachable_functions = [
        item for item in result.unreachable_items if item.code_type == "function"
    ]
    unreachable_names = [item.name for item in unreachable_functions]
    assert "unused_function" in unreachable_names
    assert "used_function" not in unreachable_names


def test_analyze_class_methods(tmp_path):
    code = """
class TestClass:
    def used_method(self):
        return 42

    def unused_method(self):
        return 24

def main():
    t = TestClass()
    return t.used_method()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)
    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(file_path), "main")

    unreachable_methods = [
        item for item in result.unreachable_items if item.code_type == "method"
    ]
    unreachable_names = [item.name for item in unreachable_methods]
    assert "TestClass.unused_method" in unreachable_names
    assert "TestClass.used_method" not in unreachable_names


def test_get_callee_name_patterns(tmp_path):
    analyzer = CodeAnalyzer(AnalyzerConfig())
    code = """
class TestClass:
    def method1(self): pass
    def method2(self): pass

class AnotherClass:
    pass

def main():
    # Direct function call
    simple_function()

    # Method call via instance
    obj = TestClass()
    obj.undefined_method()  # Method that doesn't exist in TestClass

    # Chained method call
    AnotherClass().undefined_method()  # Method that doesn't exist in AnotherClass

    # Regular calls
    TestClass().method1()
    obj.method2()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)

    with open(file_path) as f:
        tree = ast.parse(f.read())

    analyzer._analyze_module(tree, file_path)  # This populates class_instances
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

    # Test instance method call to undefined method
    assert (
        analyzer._get_callee_name(calls[2]) == "undefined_method"
    )  # Should fall back to method name

    # Test chained call to undefined method
    assert (
        analyzer._get_callee_name(calls[3]) == "undefined_method"
    )  # Should fall back to method name

    # Test defined methods (existing cases)
    assert analyzer._get_callee_name(calls[4]) == "TestClass.method1"
    assert analyzer._get_callee_name(calls[5]) == "TestClass.method2"


def test_get_callee_name_edge_cases(tmp_path):
    analyzer = CodeAnalyzer(AnalyzerConfig())
    code = """
def main():
    # Complex attribute access
    obj.attr1.attr2()

    # Unknown instance method call
    unknown_obj.method()

    # Call with no clear name
    (lambda x: x)()

    # Complex chained call
    (obj.get_something()).method()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)

    with open(file_path) as f:
        tree = ast.parse(f.read())

    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

    # Test complex attribute access
    assert analyzer._get_callee_name(calls[0]) == "attr2"

    # Test unknown instance method
    assert analyzer._get_callee_name(calls[1]) == "method"

    # Test lambda call (should return None)
    assert analyzer._get_callee_name(calls[2]) is None

    # Test complex chained call
    assert analyzer._get_callee_name(calls[3]) == "method"


def test_analyze_directory(tmp_path):
    # Create a directory with multiple Python files
    dir_path = tmp_path / "project"
    dir_path.mkdir()

    # Create main.py
    main_file = dir_path / "main.py"
    main_file.write_text(
        """
def main():
    from module import helper
    return helper()
"""
    )

    # Create module.py
    module_file = dir_path / "module.py"
    module_file.write_text(
        """
def helper():
    return 42

def unused():
    return 24
"""
    )

    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(dir_path), "main")

    unreachable_functions = [
        item for item in result.unreachable_items if item.code_type == "function"
    ]
    unreachable_names = [item.name for item in unreachable_functions]
    assert "unused" in unreachable_names
    assert "helper" not in unreachable_names


def test_analyze_invalid_path():
    analyzer = CodeAnalyzer(AnalyzerConfig())
    with pytest.raises(ValueError, match="Invalid project path:.*"):
        analyzer.analyze("nonexistent_path")


def test_analyze_cyclic_calls(tmp_path):
    code = """
def func_a():
    return func_b()

def func_b():
    return func_a()

def main():
    return func_a()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)

    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(file_path), "main")

    # Both functions should be marked as reachable despite the cycle
    assert "func_a" not in [item.name for item in result.unreachable_items]
    assert "func_b" not in [item.name for item in result.unreachable_items]


def test_analyze_undefined_function_call(tmp_path):
    code = """
def main():
    # Call to undefined function
    return nonexistent_function()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)

    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(file_path), "main")

    # Verify that main is correctly analyzed despite calling undefined function
    assert "main" not in [item.name for item in result.unreachable_items]


def test_trace_through_undefined_function(tmp_path):
    code = """
def target_function():
    return 42

def entry_function():
    # Call chain: entry_function -> undefined_function
    return undefined_function()

# Note: target_function is not called by anyone
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)

    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(file_path), "entry_function")

    # target_function should be unreachable since it's not called
    # and undefined_function is skipped during tracing
    assert "target_function" in [item.name for item in result.unreachable_items]
    assert "entry_function" not in [item.name for item in result.unreachable_items]


def test_trace_undefined_function_skipping(tmp_path):
    code = """
def main():
    # Call a builtin function
    len([1, 2, 3])
    # Call an undefined function
    undefined_func()
    # Call an "imported" function (not really imported)
    external_module.some_func()
"""
    file_path = tmp_path / "test_module.py"
    file_path.write_text(code)

    analyzer = CodeAnalyzer(AnalyzerConfig())
    result = analyzer.analyze(str(file_path), "main")

    # The worklist will contain:
    # 1. main (defined)
    # 2. len (builtin, not in defined_functions)
    # 3. undefined_func (doesn't exist)
    # 4. external_module.some_func (doesn't exist)

    # main should be reachable
    assert "main" not in [item.name for item in result.unreachable_items]
    # Analysis should complete without errors despite undefined functions
    assert isinstance(result, AnalysisResult)
