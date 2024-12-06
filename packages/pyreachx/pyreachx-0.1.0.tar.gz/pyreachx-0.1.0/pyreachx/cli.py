import click

from .analyzer import CodeAnalyzer
from .config import AnalyzerConfig
from .reporter import Reporter


@click.command()
@click.argument("project_path")
@click.option("--entry-point", "-e", help="Main entry point (e.g., module.function)")
@click.option(
    "--config", "-c", type=click.Path(exists=True), help="Path to config file"
)
@click.option("--output", "-o", default="report.html", help="Output report path")
def main(project_path, entry_point, config, output):
    """Analyze Python code reachability."""
    config = AnalyzerConfig.from_file(config) if config else AnalyzerConfig()
    analyzer = CodeAnalyzer(config)
    result = analyzer.analyze(project_path, entry_point)

    reporter = Reporter(result)
    reporter.generate_report(output)


if __name__ == "__main__":
    main()
