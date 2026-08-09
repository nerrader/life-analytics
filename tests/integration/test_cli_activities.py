from pathlib import Path

from typer.testing import CliRunner

from life_analytics import cli
from life_analytics.logic import database


def test_activities_cli_command_creates_database_entry(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test.db"

    database.create_database(temp_db_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(temp_db_path),
            "activity",
            "--activity",
            "integration testing",
            "--start",
            "20:24",
            "--end",
            "20:24",
            "--difficulty",
            "10",
            "--enjoyability",
            "10",
        ],
    )
    assert result.exit_code == 0

    data = database.fetch_activities_records(temp_db_path)
    (
        _,
        test_date,
        test_activity_name,
        test_activity_start_time,
        test_activity_end_time,
        test_activity_difficulty,
        test_activity_enjoyability,
    ) = data[0]

    assert test_date
    assert test_activity_name == "integration testing"
    assert test_activity_start_time == "20:24"
    assert test_activity_end_time == "20:24"
    assert test_activity_difficulty == 10
    assert test_activity_enjoyability == 10
