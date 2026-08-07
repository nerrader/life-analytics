from typer.testing import CliRunner

from life_analytics import cli, database


def test_activities_cli_command_creates_database_entry(tmp_path) -> None:
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
    test_activity: database.ActivityRecord = data[0]

    assert test_activity.activity == "integration testing"
    assert test_activity.activity_start == "20:24"
    assert test_activity.activity_end == "20:24"
    assert test_activity.difficulty == 10
    assert test_activity.enjoyability == 10
