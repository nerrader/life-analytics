from typer.testing import CliRunner

from life_analytics import cli, database


def test_daily_summary_cli_command_creates_database_entry(tmp_path) -> None:
    temp_db_path = tmp_path / "test.db"

    database.create_database(temp_db_path)
    cli_runner = CliRunner()

    result = cli_runner.invoke(
        cli.app,
        [
            "-db",
            str(temp_db_path),
            "summary",
            "--mood",
            "10",
            "--productivity",
            "10",
            "--stress",
            "10",
        ],
    )
    assert result.exit_code == 0

    data = database.fetch_daily_summaries_records(temp_db_path)
    test_summary: database.DailySummaryRecord = data[0]

    assert test_summary.date
    assert test_summary.mood == 10
    assert test_summary.productivity == 10
    assert test_summary.stress == 10
