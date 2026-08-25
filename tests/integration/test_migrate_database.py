from pathlib import Path

from typer.testing import CliRunner

from life_analytics.cli import app
from life_analytics.logic import database


def test_migrate_database_replaces_existing_destination(
    tmp_path: Path,
) -> None:
    old_database = tmp_path / "old.db"
    new_database = tmp_path / "new.db"

    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        app,
        ("-db", str(old_database), "sleep", "-ss", "23:00", "-se", "7:00", "-q", "4"),
    )
    assert result1.exit_code == 0

    # destination already exists, which it has to replace now
    database.create_database(new_database)

    result2 = cli_runner.invoke(
        app, ("-db", str(old_database), "migrate", "-m", str(new_database))
    )
    assert result2.exit_code == 0

    data = database.fetch_sleep_records(new_database)[0]
    assert "sleep" in data
    assert "23:00" in data[1]  # sleep start time column
    assert "7:00" in data[2]  # sleep end time column
    assert 4 in data


def test_migrate_database_in_place(
    tmp_path: Path,
) -> None:
    old_database = tmp_path / "old.db"

    cli_runner = CliRunner()

    result1 = cli_runner.invoke(
        app,
        ("-db", str(old_database), "sleep", "-ss", "23:00", "-se", "7:00", "-q", "4"),
    )
    assert result1.exit_code == 0

    result2 = cli_runner.invoke(app, ("-db", str(old_database), "migrate"))
    assert result2.exit_code == 0

    data = database.fetch_sleep_records(old_database)[0]
    assert "sleep" in data
    assert "23:00" in data[1]  # sleep start time column
    assert "7:00" in data[2]  # sleep end time column
    assert 4 in data
