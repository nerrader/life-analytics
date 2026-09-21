from datetime import datetime
from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from life_analytics.cli.app import app
from life_analytics.logic import database


def test_daily_summary_cli_command_creates_database_entry(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        app,
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

    summary_record = database.fetch_daily_summaries_records(test_database_path)[0]

    assert summary_record.summary_date
    assert summary_record.mood == 5
    assert summary_record.productivity == 5
    assert summary_record.stress == 5


def test_daily_summary_cli_command_updates_record(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        app,
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
        app,
        [
            "-db",
            str(test_database_path),
            "summary",
            "--edit",
            datetime.now().strftime("%Y-%m-%d"),
            "--mood",
            "1",
            "--stress",
            "3",
        ],
    )

    assert result2.exit_code == 0

    summary_record = database.fetch_daily_summaries_records(test_database_path)[0]

    assert summary_record.summary_date
    assert summary_record.mood == 1
    assert summary_record.productivity == 5
    assert summary_record.stress == 3


def test_daily_summary_cli_command_handles_invalid_data(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    test_database_path = tmp_path / "test.db"
    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        app,
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
    display_error_mock.assert_called_once()
