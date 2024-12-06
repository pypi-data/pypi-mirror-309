# PyReachX

PyReachX is a static code analysis tool that helps identify unreachable code in Python projects. It analyzes your Python codebase to find functions and methods that are never called or accessed.

[![CI](https://github.com/ad3002/pyreachx/actions/workflows/ci.yml/badge.svg)](https://github.com/ad3002/pyreachx/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/pyreachx.svg)](https://badge.fury.io/py/pyreachx)
[![codecov](https://codecov.io/gh/ad3002/pyreachx/branch/main/graph/badge.svg)](https://codecov.io/gh/ad3002/pyreachx)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- Identifies unreachable functions and methods
- Generates HTML and JSON reports
- Configurable exclusion patterns
- Support for class method analysis
- Command-line interface
- Confidence scoring for identified unreachable code

## Installation

```bash
pip install pyreachx
```

## Usage

### Command Line

```bash
# Basic usage
pyreachx /path/to/your/project

# Specify entry point
pyreachx /path/to/your/project -e module.main

# Custom configuration file
pyreachx /path/to/your/project -c config.yml

# Custom output file
pyreachx /path/to/your/project -o report.html
```

### Configuration

Create a `pyreachx.yml` file to customize the analysis:

```yaml
exclude_patterns:
  - "**/test_*.py"
  - "**/__init__.py"
ignore_decorators:
  - "@property"
  - "@staticmethod"
confidence_threshold: 0.8
```

### Python API

```python
from pyreachx import CodeAnalyzer, AnalyzerConfig

# Create configuration
config = AnalyzerConfig.from_file("pyreachx.yml")

# Initialize analyzer
analyzer = CodeAnalyzer(config)

# Run analysis
result = analyzer.analyze("/path/to/project", entry_point="main")

# Generate report
from pyreachx import Reporter
reporter = Reporter(result)
reporter.generate_report("report.html")
```

## Example Output

HTML Report:
```html
<div class='item'>
    <strong>module.py</strong> (lines 10-15)<br>
    Type: function<br>
    Name: unused_function<br>
    Confidence: 95%
</div>
```

JSON Report:
```json
{
    "unreachable_items": [
        {
            "file_path": "module.py",
            "line_start": 10,
            "line_end": 15,
            "code_type": "function",
            "name": "unused_function",
            "confidence": 0.95
        }
    ],
    "statistics": {
        "total_unreachable_lines": 6,
        "files_affected": ["module.py"],
        "type_distribution": {
            "function": 1
        }
    }
}
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/ad3002/pyreachx.git
cd pyreachx

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[test]
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting

```bash
# Format code
black pyreachx tests
isort pyreachx tests

# Check linting
flake8 pyreachx tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- AST module from Python standard library
- NetworkX for dependency graph analysis
- Click for CLI interface
- Jinja2 for report templating

## Project Status

PyReachX is in alpha stage. While it's functional, there might be false positives and edge cases that aren't handled yet. Use with caution in production environments.
