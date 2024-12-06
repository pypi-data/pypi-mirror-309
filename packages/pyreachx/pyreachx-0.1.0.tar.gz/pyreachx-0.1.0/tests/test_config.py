import pytest
import yaml

from pyreachx.config import AnalyzerConfig


def test_from_file_with_valid_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_content = """
    exclude_patterns:
      - "^test_.*"
    confidence_threshold: 0.9
    ignore_decorators:
      - "@property"
    """
    config_path.write_text(config_content)

    config = AnalyzerConfig.from_file(str(config_path))

    assert len(config.exclude_patterns) == 1
    assert config.exclude_patterns[0].pattern == "^test_.*"
    assert config.confidence_threshold == 0.9
    assert config.ignore_decorators == ["@property"]


def test_from_file_with_empty_file(tmp_path):
    config_path = tmp_path / "empty_config.yaml"
    config_path.write_text("")

    config = AnalyzerConfig.from_file(str(config_path))
    assert config.exclude_patterns == []
    assert config.confidence_threshold == 0.8
    assert config.ignore_decorators == []


def test_from_file_with_invalid_yaml(tmp_path):
    config_path = tmp_path / "invalid_config.yaml"
    config_path.write_text("invalid: yaml: content:")

    with pytest.raises(yaml.YAMLError):
        AnalyzerConfig.from_file(str(config_path))


def test_from_file_nonexistent():
    with pytest.raises(FileNotFoundError):
        AnalyzerConfig.from_file("nonexistent_config.yaml")


def test_from_file_invalid_regex(tmp_path):
    config_path = tmp_path / "invalid_regex_config.yaml"
    config_path.write_text(
        """
    exclude_patterns:
      - "[invalid regex"
    """
    )

    with pytest.raises(ValueError, match="Invalid regex pattern"):
        AnalyzerConfig.from_file(str(config_path))


def test_config_merge():
    # Create two configs with different settings
    config1 = AnalyzerConfig.from_dict(
        {
            "exclude_patterns": ["^test_.*", "^mock_.*"],
            "confidence_threshold": 0.8,
            "ignore_decorators": ["@property"],
        }
    )

    config2 = AnalyzerConfig.from_dict(
        {
            "exclude_patterns": ["^test_.*", "^temp_.*"],
            "confidence_threshold": 0.9,
            "ignore_decorators": ["@staticmethod", "@property"],
        }
    )

    merged = config1.merge(config2)

    # Check merged patterns (should be unique)
    patterns = {p.pattern for p in merged.exclude_patterns}
    assert patterns == {"^test_.*", "^mock_.*", "^temp_.*"}

    # Should take minimum confidence threshold
    assert merged.confidence_threshold == 0.8

    # Decorators should be unique
    assert set(merged.ignore_decorators) == {"@property", "@staticmethod"}
