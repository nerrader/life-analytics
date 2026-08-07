from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Annotated

import questionary
import typer

from life_analytics import constants as const
from life_analytics import database

app = typer.Typer()


@app.callback()
def main(
    context: typer.Context,
    database_path: Annotated[
        Path, typer.Option("--database-path", "-db", help="Path to the database file.")
    ] = const.LIFE_DATABASE_FILEPATH,
) -> None:
    """Main entry point for the CLI."""
    # this is so every command function can access the db path
    context.obj = {"database_path": database_path}

    if not database_path.exists():
        database.create_database(database_path)


def _validate_rating(value: str) -> bool | str:
    """To be passed into questionary validate keyword to validate rating questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """

    if value.isdigit() and 1 <= int(value) <= 10:
        return True
    return "Please enter a value between 1 and 10."


def _ask_rating_question(prompt_var_name: str) -> const.Rating:
    """The helper function to ask questions requiring rating in 1-10.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.

    Returns:
        str: The rating value between 1 and 10.
    """
    rating = questionary.text(
        f"Where 5 is the average, Rate your {prompt_var_name} out of 10:",
        validate=_validate_rating,
    ).ask()

    return rating


def _validate_datetime(value: str) -> bool | str:
    """To be passed into questionary validate keyword to validate datetime questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """
    try:
        datetime.strptime(value, "%H:%M")  # noqa: DTZ007
        return True
    except ValueError:
        return "Please enter a valid time in HH:MM format."


def _ask_datetime_question(prompt_var_name: str) -> str:
    """The helper function to ask questions requiring datetime in HH:MM.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.

    Returns:
        str: The datetime value in HH:MM format.
    """
    datetime_value = questionary.text(
        f"Please enter the {prompt_var_name} in HH:MM format:",
        validate=_validate_datetime,
    ).ask()

    return datetime_value


@app.command("summary")
def add_daily_summary(
    context: typer.Context,
    mood: Annotated[
        const.Rating | None,
        typer.Option("--mood", "-m", help="Your mood today (1-10)."),
    ] = None,
    productivity: Annotated[
        const.Rating | None,
        typer.Option("--productivity", "-p", help="Your productivity today (1-10)."),
    ] = None,
    stress: Annotated[
        const.Rating | None,
        typer.Option("--stress", "-s", help="Your stress level today (1-10)."),
    ] = None,
) -> None:
    """Record a daily summary entry."""
    database_path = context.obj["database_path"]
    date = datetime.now().date().isoformat()  # noqa: DTZ005

    if mood is None:
        mood = _ask_rating_question("mood")
    if productivity is None:
        productivity = _ask_rating_question("productivity")
    if stress is None:
        stress = _ask_rating_question("stress")

    database.add_daily_summary(
        database_path=database_path,
        date=date,
        mood=mood,
        productivity=productivity,
        stress=stress,
    )


@app.command("activity")
def add_activity(
    context: typer.Context,
    activity_input: Annotated[
        str | None, typer.Option("--activity", "-a", help="The activity you did today.")
    ] = None,
    activity_start_input: Annotated[
        str | None,
        typer.Option(
            "--start",
            "-st",
            help="The time you started the activity (HH:MM, 24-hour format).",
        ),
    ] = None,
    activity_end_input: Annotated[
        str | None,
        typer.Option(
            "--end",
            "-e",
            help="The time you ended the activity (HH:MM, 24-hour format).",
        ),
    ] = None,
    difficulty: Annotated[
        const.Rating | None,
        typer.Option(
            "--difficulty", "-d", help="The difficulty of the activity (1-10)."
        ),
    ] = None,
    enjoyability: Annotated[
        const.Rating | None,
        typer.Option(
            "--enjoyability", "-en", help="The enjoyability of the activity (1-10)."
        ),
    ] = None,
) -> None:
    """Record an activity entry."""
    database_path = context.obj["database_path"]
    date = datetime.now().date().isoformat()  # noqa: DTZ005

    if activity_input is not None and activity_input.strip():
        activity = activity_input

    else:
        activity: str = questionary.text(
            "What activity did you do today?",
            validate=lambda text: (
                True if text.strip() else "Please enter a valid activity."
            ),
        ).ask()

    # i do this instead of questionarys skip if because it doesnt work in tests
    if (
        activity_start_input is not None
        and _validate_datetime(activity_start_input) is True
    ):
        activity_start = activity_start_input
    else:
        activity_start: str = _ask_datetime_question("activity start time")

    # i do this instead of questionarys skip if because it doesnt work in tests
    if (
        activity_end_input is not None
        and _validate_datetime(activity_end_input) is True
    ):
        activity_end = activity_end_input
    else:
        activity_end: str = _ask_datetime_question("activity end time")

    if difficulty is None:
        difficulty = _ask_rating_question("difficulty")
    if enjoyability is None:
        enjoyability = _ask_rating_question("enjoyability")

    database.add_activity(
        database_path=database_path,
        date=date,
        activity=activity,
        activity_start=activity_start,
        activity_end=activity_end,
        difficulty=difficulty,
        enjoyability=enjoyability,
    )


@app.command("sleep")
def add_sleep(
    context: typer.Context,
    sleep_start_input: Annotated[
        str | None,
        typer.Option(
            "--start",
            "-st",
            help="The time you went to sleep yesterday (HH:MM, 24-hour format).",
        ),
    ] = None,
    sleep_end_input: Annotated[
        str | None,
        typer.Option(
            "--end", "-e", help="The time you woke up today (HH:MM, 24-hour format)."
        ),
    ] = None,
    sleep_quality: Annotated[
        const.Rating | None,
        typer.Option("--quality", "-q", help="The quality of your sleep (1-10)."),
    ] = None,
) -> None:
    """Record a sleep entry."""
    database_path = context.obj["database_path"]
    today_date = datetime.now()  # noqa: DTZ005
    yesterday_date = today_date - timedelta(days=1)

    # i do this instead of questionarys skip if because it doesnt work in tests
    if sleep_start_input is not None and _validate_datetime(sleep_start_input) is True:
        start_sleep_time = sleep_start_input
    else:
        start_sleep_time: str = _ask_datetime_question("your sleep start time")

    # change it to a time object
    polished_start_sleep_time: time = datetime.strptime(  # noqa: DTZ007
        start_sleep_time, "%H:%M"
    ).time()

    # so we can use it to replace the hour and minute of the generated yesterdays date
    sleep_start_datetime = yesterday_date.replace(
        hour=polished_start_sleep_time.hour,
        minute=polished_start_sleep_time.minute,
    ).isoformat(timespec="minutes")

    # i do this instead of questionarys skip if because it doesnt work in tests
    if sleep_end_input is not None and _validate_datetime(sleep_end_input) is True:
        end_sleep_time = sleep_end_input
    else:
        end_sleep_time: str = _ask_datetime_question("your sleep end time")

    # change it to a time object
    polished_end_sleep_time: time = datetime.strptime(end_sleep_time, "%H:%M").time()  # noqa: DTZ007

    # so we can use it to replace the hour and minute of the generated yesterdays date
    sleep_end_datetime: str = today_date.replace(
        hour=polished_end_sleep_time.hour,
        minute=polished_end_sleep_time.minute,
    ).isoformat(timespec="minutes")

    if sleep_quality is None:
        sleep_quality = _ask_rating_question("sleep_quality")

    database.add_sleep(
        database_path=database_path,
        sleep_start_datetime=sleep_start_datetime,
        sleep_end_datetime=sleep_end_datetime,
        sleep_quality=sleep_quality,
    )


@app.command("stats")
def show_stats() -> None:
    raise NotImplementedError("The 'stats' command is not yet implemented.")


@app.command("clear")
def clear_all_data(
    skip_confirm: Annotated[
        bool | None, typer.Option("--skip", "-s", help="Skips the confirmation prompt.")
    ] = None,
) -> None:
    """Removes all tracking data from the database.

    Args:
        skip_confirm (bool, Optional): If this flag is invoked, it skips the confirmation prompt.
    """

    clear_data_confirm = (
        questionary.confirm(
            "Are you sure you want to clear all data from the database?"
        )
        .skip_if(skip_confirm is True, default=True)
        .ask()
    )

    if clear_data_confirm:
        database.clear_database(const.LIFE_DATABASE_FILEPATH)
