import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Pattern

import yaml


@dataclass
class AnalyzerConfig:
    exclude_patterns: List[Pattern] = field(default_factory=list)
    confidence_threshold: float = 0.8
    ignore_decorators: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalyzerConfig":
        exclude_patterns = []
        for pattern_str in data.get("exclude_patterns", []):
            try:
                compiled_pattern = re.compile(pattern_str)
                exclude_patterns.append(compiled_pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern_str}': {e}")
        return cls(
            exclude_patterns=exclude_patterns,
            confidence_threshold=data.get("confidence_threshold", 0.8),
            ignore_decorators=data.get("ignore_decorators", []),
        )

    @classmethod
    def from_file(cls, config_path: str) -> "AnalyzerConfig":
        with open(config_path) as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data or {})

    def merge(self, other: "AnalyzerConfig") -> "AnalyzerConfig":
        return AnalyzerConfig(
            exclude_patterns=list(set(self.exclude_patterns + other.exclude_patterns)),
            confidence_threshold=min(
                self.confidence_threshold, other.confidence_threshold
            ),
            ignore_decorators=list(
                set(self.ignore_decorators + other.ignore_decorators)
            ),
        )
