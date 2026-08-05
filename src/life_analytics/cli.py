from datetime import datetime, time, timedelta
from typing import Annotated

import questionary
import typer

from life_analytics import constants as const
from life_analytics import database

app = typer.Typer()


def _validate_rating(value: str) -> bool | str:
    if value.isdigit() and 1 <= int(value) <= 10:
        return True
    return "Please enter a value between 1 and 10."


def _ask_rating_question(var_name: str) -> const.Rating:
    rating = questionary.text(
        f"Where 5 is the average, Rate your {var_name} out of 10:",
        validate=_validate_rating,
    ).ask()

    return rating


def _validate_datetime(value: str) -> bool | str:
    try:
        datetime.strptime(value, "%H:%M")  # noqa: DTZ007
        return True
    except ValueError:
        return "Please enter a valid time in HH:MM format."


def _ask_datetime_question(prompt_var_name: str, skip_if_var: str | None) -> str:
    datetime_value = (
        questionary.text(
            f"Please enter the {prompt_var_name} in HH:MM format:",
            validate=_validate_datetime,
        )
        .skip_if(
            skip_if_var is not None and _validate_datetime(skip_if_var) is True,
            default=skip_if_var,
        )
        .ask()
    )

    return datetime_value


@app.command("summary")
def add_daily_summary(
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
    date = datetime.now().date().isoformat()  # noqa: DTZ005

    if mood is None:
        mood = _ask_rating_question("mood")
    if productivity is None:
        productivity = _ask_rating_question("productivity")
    if stress is None:
        stress = _ask_rating_question("stress")

    database.add_daily_summary(
        database_path=const.LIFE_DATABASE_FILEPATH,
        date=date,
        mood=mood,
        productivity=productivity,
        stress=stress,
    )


@app.command("activity")
def add_activity(
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
    date = datetime.now().date().isoformat()  # noqa: DTZ005

    activity: str = (
        questionary.text(
            "What activity did you do today?",
            validate=lambda text: (
                True if text.strip() else "Please enter a valid activity."
            ),
        )
        .skip_if(
            activity_input is not None and bool(activity_input.strip()),
            default=activity_input,
        )
        .ask()
    )

    activity_start: str = _ask_datetime_question(
        "activity start time", activity_start_input
    )
    activity_end: str = _ask_datetime_question("activity end time", activity_end_input)

    if difficulty is None:
        difficulty = _ask_rating_question("difficulty")
    if enjoyability is None:
        enjoyability = _ask_rating_question("enjoyability")

    database.add_activity(
        database_path=const.LIFE_DATABASE_FILEPATH,
        date=date,
        activity=activity,
        activity_start=activity_start,
        activity_end=activity_end,
        difficulty=difficulty,
        enjoyability=enjoyability,
    )


@app.command("sleep")
def add_sleep(
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
    today_date = datetime.now()  # noqa: DTZ005
    yesterday_date = today_date - timedelta(days=1)

    start_sleep_time: time = datetime.strptime(  # noqa: DTZ007
        _ask_datetime_question("your sleep start time", sleep_start_input),
        "%H:%M",
    ).time()

    sleep_start_datetime = yesterday_date.replace(
        hour=start_sleep_time.hour,
        minute=start_sleep_time.minute,
    ).isoformat(timespec="minutes")

    end_sleep_time: time = datetime.strptime(  # noqa: DTZ007
        _ask_datetime_question("your sleep end time", sleep_end_input),
        "%H:%M",
    ).time()

    sleep_end_datetime: str = today_date.replace(
        hour=end_sleep_time.hour,
        minute=end_sleep_time.minute,
    ).isoformat(timespec="minutes")

    if sleep_quality is None:
        sleep_quality = _ask_rating_question("sleep_quality")

    database.add_sleep(
        database_path=const.LIFE_DATABASE_FILEPATH,
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
