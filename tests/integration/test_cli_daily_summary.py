from datetime import datetime
from pathlib import Path

from typer.testing import CliRunner

from life_analytics import cli
from life_analytics.logic import database


def test_daily_summary_cli_command_creates_database_entry(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "summary",
            "--mood",
            "5",
            "--productivity",
            "5",
            "--stress",
            "5",
        ],
    )
    assert result.exit_code == 0

    data = database.fetch_daily_summaries_records(test_database_path)
    test_date, test_mood, test_productivity, test_stress = data[0]

    assert test_date
    assert test_mood == 5
    assert test_productivity == 5
    assert test_stress == 5


def test_daily_summary_cli_command_updates_record(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "summary",
            "--mood",
            "5",
            "--productivity",
            "5",
            "--stress",
            "5",
        ],
    )

    assert result1.exit_code == 0

    result2 = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "summary",
            "--edit",
            datetime.now().strftime("%Y-%m-%d"),  # noqa: DTZ005
            "--mood",
            "1",
            "--stress",
            "3",
        ],
    )

    assert result2.exit_code == 0

    data = database.fetch_daily_summaries_records(test_database_path)
    test_date, test_mood, test_productivity, test_stress = data[0]

    assert test_date
    assert test_mood == 1
    assert test_productivity == 5
    assert test_stress == 3


def test_daily_summary_cli_command_handles_invalid_data(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "summary",
            "--mood",
            "10",
            "--productivity",
            "5",
            "--stress",
            "5",
        ],
    )

    assert result.exit_code == 0
    assert "ERROR:" in result.stdout
