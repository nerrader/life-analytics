from datetime import datetime
from typing import Annotated

import questionary
import typer

from life_analytics import constants as const
from life_analytics import database

app = typer.Typer()


def _get_current_date_isostring() -> str:
    return datetime.now().date().isoformat()  # noqa: DTZ005


def _ask_rating_question(var_name: str) -> const.Rating:
    def validate_rating(value: str) -> bool | str:
        if value.isdigit() and 1 <= int(value) <= 10:
            return True
        return "Please enter a value between 1 and 10."

    rating = questionary.text(
        f"Where 5 is the average, Rate your {var_name} out of 10:",
        validate=validate_rating,
    ).ask()

    return rating


def _validate_datetime(value: str) -> bool | str:
    try:
        datetime.strptime(value, "%H:%M")  # noqa: DTZ007
        return True
    except ValueError:
        return "Please enter a valid time in HH:MM format."


@app.command("summary")
def add_daily_summary() -> None:
    """Prompts for data, then inserts the daily summary in the database."""
    date = _get_current_date_isostring()

    mood = _ask_rating_question("mood")
    productivity = _ask_rating_question("productivity")
    stress = _ask_rating_question("stress")

    database.add_daily_summary(
        const.LIFE_DATABASE_FILEPATH,
        date,
        mood,
        productivity,
        stress,
    )


@app.command("activity")
def add_activity() -> None:
    date = _get_current_date_isostring()

    activity = questionary.text(
        "What activity did you do today?",
        validate=lambda text: (
            True if text.strip() else "Please enter a valid activity."
        ),
    ).ask()

    activity_start = questionary.text(
        "What time did you start the activity? (HH:MM, 24-hour format)",
        validate=_validate_datetime,
    ).ask()

    activity_end = questionary.text(
        "What time did you end the activity? (HH:MM, 24-hour format)",
        validate=_validate_datetime,
    ).ask()

    difficulty = _ask_rating_question("difficulty")
    enjoyability = _ask_rating_question("enjoyability")

    database.add_activity(
        const.LIFE_DATABASE_FILEPATH,
        date,
        activity,
        activity_start,
        activity_end,
        difficulty,
        enjoyability,
    )


@app.command("sleep")
def add_sleep() -> None:
    pass


@app.command("stats")
def show_stats() -> None:
    pass


@app.command("clear")
def clear_all_data(
    skip_confirm: Annotated[
        bool | None, typer.Option("--skip", "-s", help="Skips the confirmation prompt.")
    ] = None,
) -> None:

    clear_data_confirm = questionary.confirm(
        "Are you sure you want to clear all data from the database?"
    ).skip_if(skip_confirm == True, default=True)

    if clear_data_confirm:
        database.clear_database(const.LIFE_DATABASE_FILEPATH)
