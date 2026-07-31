from datetime import datetime
from typing import Annotated

import questionary
import typer

from life_analytics import constants as const
from life_analytics import database

app = typer.Typer()


def _get_current_datetime_isostring() -> str:
    return datetime.now().astimezone().isoformat()


def ask_rating_question(var_name: str) -> const.Rating:

    def validate_rating(value: str) -> bool | str:
        if value.isdigit() and 1 <= int(value) <= 10:
            return True
        return "Please enter a value between 1 and 10."

    rating = questionary.text(
        f"Where 5 is the average, Rate your {var_name} out of 10:",
        validate=validate_rating,
    ).ask()

    return rating


@app.command("summary")
def add_daily_summary() -> None:
    """Prompts for data, then inserts the daily summary in the database."""
    date = _get_current_datetime_isostring()

    outside_for_leisure_minutes = questionary.text(
        "How many minutes were you outside today during your free time?",
        validate=lambda text: (
            True if text.isdigit() else "Please enter a valid number."
        ),
    ).ask()

    exercise_minutes = questionary.text(
        "How many minutes did you exercise for today?",
        validate=lambda text: (
            True if text.isdigit() else "Please enter a valid number."
        ),
    ).ask()

    mood = ask_rating_question("mood")
    productivity = ask_rating_question("productivity")
    stress = ask_rating_question("stress")

    database.add_daily_summary(
        const.LIFE_DATABASE_FILEPATH,
        date,
        outside_for_leisure_minutes,
        exercise_minutes,
        mood,
        productivity,
        stress,
    )


@app.command("activity")
def add_activity() -> None:
    pass


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
