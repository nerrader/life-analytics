from pathlib import Path

from typer.testing import CliRunner

from life_analytics import cli
from life_analytics.logic import database


def test_activities_cli_command_creates_database_entry(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "activity",
            "--category",
            "DEV",
            "--description",
            "integration testing",
            "--start",
            "20:24",
            "--end",
            "20:24",
            "--effort",
            "5",
            "--enjoyability",
            "5",
            "--energy-before",
            "5",
            "--energy-after",
            "5",
        ],
    )
    assert result.exit_code == 0

    activity_record = database.fetch_activities_records(test_database_path)[0]

    assert activity_record.activity_category == "DEV"
    assert activity_record.activity_description == "integration testing"
    assert activity_record.effort == 5
    assert activity_record.energy_after == 5


def test_activities_cli_command_updates_record(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"

    database.create_database(test_database_path)
    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "activity",
            "--category",
            "IDLE",
            "--description",
            "integration testing",
            "--start",
            "20:24",
            "--end",
            "20:24",
            "--effort",
            "5",
            "--enjoyability",
            "5",
            "--energy-before",
            "1",
            "--energy-after",
            "3",
        ],
    )
    assert result1.exit_code == 0

    result2 = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "activity",
            "--edit",
            "1",
            "--effort",
            "1",
            "--energy-before",
            "5",
            "--enjoyability",
            "1",
            "--category",
            "DEV",
        ],
    )
    assert result2.exit_code == 0

    activity_record = database.fetch_activities_records(test_database_path)[0]
    assert activity_record.effort == 1
    assert activity_record.energy_before == 5
    assert activity_record.energy_after == 3
    assert activity_record.activity_category == "DEV"


def test_activity_cli_command_handles_invalid_data(tmp_path: Path) -> None:
    test_database_path = tmp_path / "test.db"
    database.create_database(test_database_path)

    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(test_database_path),
            "activity",
            "-ac",
            "DEV",
            "-ad",
            "integration testing invalid values",
            "-as",
            "99:99",
            "-ae",
            "99:99",
            "-ef",
            "5",
            "-en",
            "-500",
            "-eb",
            "5",
            "-ea",
            "5",
        ],
    )

    assert result.exit_code == 0, (result.output, result.exception)
    assert "ERROR:" in result.stdout
