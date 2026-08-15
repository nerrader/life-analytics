from pathlib import Path

from typer.testing import CliRunner

from life_analytics import cli
from life_analytics.logic import database


def test_sleep_cli_command_creates_database_entry(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "sleep",
            "--start",
            "21:00",
            "--end",
            "06:00",
            "--quality",
            "5",
            "--nap",
        ],
    )
    assert result.exit_code == 0

    data = database.fetch_sleep_records(test_database_path)
    _, test_sleep_start, test_sleep_end, test_sleep_quality, test_sleep_type = data[0]

    # time in the sleep database in stored in YYYY-MM-DDTHH:MM which is why im using onnly the time here
    assert "21:00" in test_sleep_start
    assert "6:00" in test_sleep_end
    assert test_sleep_quality == 5
    assert test_sleep_type == "nap"


def test_sleep_cli_command_updates_record(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "sleep",
            "--start",
            "21:00",
            "--end",
            "06:00",
            "--quality",
            "5",
        ],
    )
    assert result1.exit_code == 0

    result2 = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "sleep",
            "--edit",
            "1",
            "--quality",
            "1",
        ],
    )
    assert result2.exit_code == 0

    data = database.fetch_sleep_records(test_database_path)
    _, test_sleep_start, test_sleep_end, test_sleep_quality, test_sleep_type = data[0]

    # time in the sleep database in stored in YYYY-MM-DDTHH:MM which is why im using only the time here
    assert "21:00" in test_sleep_start
    assert "6:00" in test_sleep_end
    assert test_sleep_quality == 1
    assert test_sleep_type == "sleep"


def test_sleep_cli_command_handles_invalid_values(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "sleep",
            "--start",
            "21:00",
            "--end",
            "06:00",
            "--quality",
            "-500",
        ],
    )
    assert result.exit_code == 0
    assert "ERROR:" in result.stdout
