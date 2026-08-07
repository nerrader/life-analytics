from typer.testing import CliRunner

from life_analytics import cli
from life_analytics.logic import database


def test_sleep_cli_command_creates_database_entry(tmp_path) -> None:
    temp_db_path = tmp_path / "test.db"

    database.create_database(temp_db_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(temp_db_path),
            "sleep",
            "--start",
            "21:00",
            "--end",
            "06:00",
            "--quality",
            "10",
        ],
    )
    assert result.exit_code == 0

    data = database.fetch_sleep_records(temp_db_path)
    test_summary: database.SleepRecord = data[0]

    # time in the sleep database in stored in YYYY-MM-DDTHH:MM which is why im using onnly the time here
    assert "21:00" in test_summary.sleep_start_time
    assert "06:00" in test_summary.sleep_end_time
    assert test_summary.sleep_quality == 10
