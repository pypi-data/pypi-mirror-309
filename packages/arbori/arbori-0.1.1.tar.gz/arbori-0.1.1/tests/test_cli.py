from click.testing import CliRunner

from arbori.cli import arbori


def test_cli_invalid_input_path_fail(tmp_path):
    invalid_input_file = tmp_path / "non_existent_input.txt"
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(arbori, [str(invalid_input_file), str(output_dir)])

    assert result.exit_code != 0
    assert "Invalid value for 'INPUT'" in result.output


def test_cli_invalid_output_path_fail(tmp_path):
    input_file = tmp_path / "input.txt"
    with open(input_file, "w") as f:
        f.write("root\n  child1\n    grandchild1\n")
    invalid_output_dir = tmp_path / "non_existent_output"

    runner = CliRunner()
    result = runner.invoke(arbori, [str(input_file), str(invalid_output_dir)])

    assert result.exit_code != 0
    assert "Invalid value for 'OUTPUT': Directory" in result.output


def test_cli_valid_input_pass(tmp_path):
    input_file = tmp_path / "input.txt"
    with open(input_file, "w") as f:
        f.write("root\n  child1\n    grandchild1\n")
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(arbori, [str(input_file), str(output_dir)])

    assert result.exit_code == 0
    assert (output_dir / "root" / "child1" / "grandchild1").exists()


def test_cli_help_option_pass():
    expected_result = (
        """
Usage: arbori [OPTIONS] INPUT OUTPUT

  Create a directory structure given a simple input format

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
"""
    ).strip()

    runner = CliRunner()
    result = runner.invoke(arbori, ["--help"])

    assert result.exit_code == 0
    assert expected_result in result.output
