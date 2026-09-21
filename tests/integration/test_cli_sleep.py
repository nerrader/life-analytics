from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from life_analytics.cli.app import app
from life_analytics.logic import database


def test_sleep_cli_command_creates_database_entry(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        app,
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
            "--type",
            "nap",
        ],
    )
    assert result.exit_code == 0

    sleep_record = database.fetch_sleep_records(test_database_path)[0]

    # time in the sleep database in stored in YYYY-MM-DDTHH:MM which is why im using only the time here
    assert "21:00" in sleep_record.start_at
    assert "6:00" in sleep_record.end_at
    assert sleep_record.quality == 5
    assert sleep_record.sleep_type == "nap"


def test_sleep_cli_command_updates_record(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        app,
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
        app,
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

    sleep_record = database.fetch_sleep_records(test_database_path)[0]

    # time in the sleep database is stored as YYYY-MM-DDTHH:MM which is why im using only the time here
    assert "21:00" in sleep_record.start_at
    assert "6:00" in sleep_record.end_at
    assert sleep_record.quality == 1
    assert sleep_record.sleep_type == "sleep"


def test_sleep_cli_command_handles_invalid_values(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    result = cli_runner.invoke(
        app,
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
    display_error_mock.assert_called_once()
    assert result.exit_code == 0


def test_sleep_cli_command_edit_detailed_flag_works(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        app,
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
        app,
        [
            "-db",
            str(test_database_path),
            "sleep",
            "--edit",
            "1",
            "--detailed",
            "--start",
            "2026-09-15 20:59",
            "--end",
            "2026-09-15 21:00",
            "--quality",
            "1",
        ],
    )
    assert result2.exit_code == 0

    sleep_record = database.fetch_sleep_records(test_database_path)[0]
    assert sleep_record.start_at == "2026-09-15T20:59"
    assert sleep_record.end_at == "2026-09-15T21:00"
    assert sleep_record.quality == 1


def test_sleep_cli_command_detailed_flag_is_invalid_value_displays_error_diagnostics(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    result = cli_runner.invoke(
        app,
        [
            "-db",
            str(test_database_path),
            "sleep",
            "--detailed",
            "--start",
            "2026-09-15 20:59",
            "--end",
            "2026-200-15 21:00",
            "--quality",
            "5",
        ],
    )
    assert result.exit_code == 0
    display_error_mock.assert_called_once()
