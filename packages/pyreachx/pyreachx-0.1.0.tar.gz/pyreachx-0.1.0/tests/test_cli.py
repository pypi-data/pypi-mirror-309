from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from pyreachx.cli import main


def test_main_no_arguments():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 2
    assert "Missing argument" in result.output


@patch("pyreachx.cli.CodeAnalyzer")
def test_main_with_project_path(mock_analyzer):
    mock_analyzer.return_value.analyze.return_value = MagicMock()
    runner = CliRunner()
    result = runner.invoke(main, ["project_path"], standalone_mode=False)
    assert result.exit_code == 0

    # Verify analyzer was created and used correctly
    mock_analyzer.assert_called_once()
    mock_analyzer.return_value.analyze.assert_called_once_with("project_path", None)


@patch("pyreachx.cli.CodeAnalyzer")
@patch("pyreachx.cli.AnalyzerConfig")
@patch("pyreachx.cli.Reporter")
def test_main_with_options(mock_reporter, mock_config, mock_analyzer):
    mock_analyzer.return_value.analyze.return_value = MagicMock()
    mock_config.from_file.return_value = MagicMock()
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a dummy config file
        with open("config.yaml", "w") as f:
            f.write("dummy: config")

        result = runner.invoke(
            main,
            [
                "project_path",
                "--entry-point",
                "module.function",
                "--config",
                "config.yaml",
                "--output",
                "report.html",
            ],
            standalone_mode=False,
        )

        assert result.exit_code == 0

        # Verify config was loaded
        mock_config.from_file.assert_called_once_with("config.yaml")

        # Verify analyzer was created and used correctly
        mock_analyzer.assert_called_once_with(mock_config.from_file.return_value)
        mock_analyzer.return_value.analyze.assert_called_once_with(
            "project_path", "module.function"
        )

        # Verify reporter was created and used correctly
        mock_reporter.assert_called_once_with(
            mock_analyzer.return_value.analyze.return_value
        )
        mock_reporter.return_value.generate_report.assert_called_once_with(
            "report.html"
        )


def test_cli_as_script():
    import subprocess
    import sys
    from pathlib import Path

    # Get the package directory
    package_dir = Path(__file__).parent.parent

    # Run using python -m
    process = subprocess.run(
        [sys.executable, "-m", "pyreachx.cli"],
        capture_output=True,
        text=True,
        cwd=str(package_dir),
    )

    # Verify the script ran and produced the expected usage error
    assert process.returncode == 2
    assert "Usage:" in process.stderr
    assert "Missing argument" in process.stderr
