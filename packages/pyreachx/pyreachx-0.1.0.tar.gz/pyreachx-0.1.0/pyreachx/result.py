from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UnreachableCode:
    file_path: str
    line_start: int
    line_end: int
    code_type: str
    name: str
    confidence: float


class AnalysisResult:
    def __init__(self):
        self.unreachable_items: List[UnreachableCode] = []
        self.statistics: Dict = {
            "total_unreachable_lines": 0,
            "files_affected": set(),
            "type_distribution": {},
        }
        self.unreachable_functions: List[UnreachableCode] = []
        self.unreachable_methods: List[UnreachableCode] = []

    def add_item(self, item: UnreachableCode):
        self.unreachable_items.append(item)
        self.statistics["files_affected"].add(item.file_path)
        self.statistics["type_distribution"][item.code_type] = (
            self.statistics["type_distribution"].get(item.code_type, 0) + 1
        )
        if item.code_type == "function":
            self.unreachable_functions.append(item)
        elif item.code_type == "method":
            self.unreachable_methods.append(item)
