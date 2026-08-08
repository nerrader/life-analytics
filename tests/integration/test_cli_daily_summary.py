from typer.testing import CliRunner

from life_analytics import cli
from life_analytics.logic import database


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
    test_date, test_mood, test_productivity, test_stress = data[0]

    assert test_date
    assert test_mood == 10
    assert test_productivity == 10
    assert test_stress == 10
