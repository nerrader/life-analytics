from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from life_analytics.cli import app
from life_analytics.logic import database


def test_end_activity_no_activity_started(tmp_path: Path) -> None:
    """Ending an activity without starting one should fail."""

    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "-db",
            str(tmp_path / "temp.db"),
            "end",
            "--category",
            "DEV",
        ],
    )

    assert result.exit_code != 0


def test_end_activity_uses_cli_options_without_prompting(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    """Explicit CLI values should be used instead of prompting for them."""

    start_file = tmp_path / "activity_start.txt"
    start_file.write_text("2026-09-12T08:00")

    category_mock = mocker.patch("life_analytics.cli.prompts.ask_activity_category")
    category_mock.return_value = "SCHOOL"
    description_mock = mocker.patch(
        "life_analytics.cli.prompts.ask_activity_description"
    )
    description_mock.return_value = "integration testing"
    rating_mock = mocker.patch("life_analytics.cli.prompts.ask_rating_question")

    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "-db",
            str(tmp_path / "test.db"),
            "-ap",
            str(tmp_path / "activity_start.txt"),
            "end",
            "--effort",
            "3",
            "--enjoyability",
            "4",
            "--energy-before",
            "5",
            "--energy-after",
            "2",
        ],
    )

    assert result.exit_code == 0

    category_mock.assert_called_once()
    description_mock.assert_called_once()

    # No rating prompts should be necessary when all ratings were supplied.
    rating_mock.assert_not_called()

    activity_record = database.fetch_activities_records(tmp_path / "test.db")[0]
    assert activity_record.activity_category == "SCHOOL"
    assert activity_record.activity_description == "integration testing"
    assert activity_record.enjoyability == 4
    assert activity_record.energy_before == 5
    assert activity_record.energy_after == 2
