from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

import typer

from life_analytics import constants as const
from life_analytics import database, prompts, time_utils

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

    mood = mood or prompts.ask_rating_question("mood")
    productivity = productivity or prompts.ask_rating_question("productivity")
    stress = stress or prompts.ask_rating_question("stress")

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

    activity = prompts.ask_activity_name("What did you do today?", activity_input)

    activity_start = prompts.ask_datetime_question(
        "activity start time", activity_start_input
    )

    activity_end: str = prompts.ask_datetime_question(
        "activity end time", activity_end_input
    )

    difficulty = difficulty or prompts.ask_rating_question("difficulty")
    enjoyability = enjoyability or prompts.ask_rating_question("enjoyability")

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

    start_sleep_time: str = prompts.ask_datetime_question(
        "your sleep start time", sleep_start_input
    )
    sleep_start_datetime = time_utils.combine_date_and_time(
        start_sleep_time, yesterday_date
    ).isoformat(timespec="minutes")

    end_sleep_time: str = prompts.ask_datetime_question(
        "your sleep end time", sleep_end_input
    )
    sleep_end_datetime = time_utils.combine_date_and_time(
        end_sleep_time, today_date
    ).isoformat(timespec="minutes")

    sleep_quality = sleep_quality or prompts.ask_rating_question("sleep quality")

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

    clear_data_confirm = prompts.ask_for_confirmation(
        "Are you sure you want to clear the database?", skip_confirm
    )

    if clear_data_confirm:
        database.clear_database(const.LIFE_DATABASE_FILEPATH)
