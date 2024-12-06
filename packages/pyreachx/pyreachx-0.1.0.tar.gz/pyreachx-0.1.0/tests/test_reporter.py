import json

from pyreachx.reporter import Reporter
from pyreachx.result import AnalysisResult, UnreachableCode


def test_html_report_generation(tmp_path):
    result = AnalysisResult()
    result.add_item(
        UnreachableCode(
            file_path="test.py",
            line_start=10,
            line_end=15,
            code_type="function",
            name="unused_function",
            confidence=0.95,
        )
    )
    reporter = Reporter(result)
    output_path = tmp_path / "report.html"
    reporter.generate_html(str(output_path))
    assert output_path.exists()


def test_json_report_generation(tmp_path):
    result = AnalysisResult()
    result.add_item(
        UnreachableCode(
            file_path="test.py",
            line_start=20,
            line_end=25,
            code_type="method",
            name="unused_method",
            confidence=0.90,
        )
    )
    reporter = Reporter(result)
    output_path = tmp_path / "report.json"
    reporter.generate_json(str(output_path))
    assert output_path.exists()


def test_generate_report_json(tmp_path):
    result = AnalysisResult()
    result.add_item(
        UnreachableCode(
            file_path="test.py",
            line_start=20,
            line_end=25,
            code_type="method",
            name="unused_method",
            confidence=0.90,
        )
    )

    reporter = Reporter(result)
    output_path = tmp_path / "report.json"

    # Test generate_report with .json extension
    reporter.generate_report(str(output_path))

    # Verify JSON file was created and has correct content
    assert output_path.exists()
    with open(output_path) as f:
        report_data = json.load(f)
        assert "unreachable_items" in report_data
        assert "statistics" in report_data
        assert report_data["unreachable_items"][0]["name"] == "unused_method"
