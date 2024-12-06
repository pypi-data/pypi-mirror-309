import json
from typing import Any, Dict

from .result import AnalysisResult


class Reporter:
    def __init__(self, result: AnalysisResult):
        self.result = result

    def generate_html(self, output_path: str):
        """Generate HTML report at the specified path."""
        html_content = self._generate_html()
        with open(output_path, "w") as f:
            f.write(html_content)

    def generate_json(self, output_path: str):
        """Generate JSON report at the specified path."""
        report = {
            "unreachable_items": [
                item.__dict__ for item in self.result.unreachable_items
            ],
            "statistics": self._get_statistics(),
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=4)

    def generate_report(self, output_path: str):
        """Generate report in the appropriate format based on file extension."""
        if output_path.endswith(".json"):
            self.generate_json(output_path)
        else:
            self.generate_html(output_path)

    def _get_statistics(self) -> Dict[str, Any]:
        return {
            "total_unreachable_lines": sum(
                item.line_end - item.line_start + 1
                for item in self.result.unreachable_items
            ),
            "files_affected": list(self.result.statistics["files_affected"]),
            "type_distribution": self.result.statistics["type_distribution"],
        }

    def _generate_html(self) -> str:
        stats = self._get_statistics()
        html_content = """
        <html>
            <head>
                <title>Analysis Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .item { margin: 10px 0; padding: 5px; border: 1px solid #eee; }
                </style>
            </head>
            <body>
        """
        html_content += "<h1>Unreachable Code Analysis Report</h1>"
        html_content += "<h2>Summary Statistics</h2>"
        html_content += "<p>Total Unreachable Lines: {}</p>".format(
            stats["total_unreachable_lines"]
        )
        html_content += f"<p>Files Affected: {len(stats['files_affected'])}</p>"

        # Add type distribution
        html_content += "<h2>Type Distribution</h2><ul>"
        for code_type, count in stats["type_distribution"].items():
            html_content += f"<li>{code_type}: {count}</li>"
        html_content += "</ul>"

        # Add unreachable items
        html_content += "<h2>Unreachable Items</h2>"
        for item in self.result.unreachable_items:
            html_content += f"""
            <div class='item'>
                <strong>{item.file_path}</strong>
                  (lines {item.line_start}-{item.line_end})<br>
                Type: {item.code_type}<br>
                Name: {item.name}<br>
                Confidence: {item.confidence:.2%}
            </div>
            """

        html_content += "</body></html>"
        return html_content
