import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Final

import typer
from rich.console import Console

from life_analytics import __version__
from life_analytics import constants as const
from life_analytics.logic import database, prompts, tables, time_utils

app = typer.Typer()

console = Console()

VALID_TABLE_TYPES: Final[tuple[str, ...]] = ("summary", "activity", "sleep")


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    database_path: Annotated[
        Path, typer.Option("--database-path", "-db", help="Path to the database file.")
    ] = const.DEFAULT_DATABASE_PATH,
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Displays the version")
    ] = False,
) -> None:
    """Main entry point for the CLI."""
    # this is so every command function can access the db path
    context.obj = {"database_path": database_path}

    if version:
        print(__version__)
        return

    if not database_path.exists():
        database.create_database(database_path)


@app.command("summary")
def add_daily_summary(
    context: typer.Context,
    edit: Annotated[
        str | None,
        typer.Option(
            "--edit",
            "-e",
            help="The record's date that you want updated in YYYY-MM-DD format.",
        ),
    ] = None,
    mood: Annotated[
        float | None,
        typer.Option("--mood", "-m", help="Your mood today (1-5)."),
    ] = None,
    productivity: Annotated[
        float | None,
        typer.Option("--productivity", "-p", help="Your productivity today (1-5)."),
    ] = None,
    stress: Annotated[
        float | None,
        typer.Option("--stress", "-s", help="Your stress level today (1-5)."),
    ] = None,
) -> None:
    """Record a daily summary entry."""
    database_path = context.obj["database_path"]

    if edit:
        try:
            database.update_daily_summary_record(
                database_path,
                edit,
                {"mood": mood, "productivity": productivity, "stress": stress},
            )
        except ValueError as error:
            console.print(f"ERROR: {error}", style="red")
            return

        except sqlite3.IntegrityError:
            console.print(
                "ERROR: Failed to update record: Invalid values were passed to the database."
            )
        return

    date = datetime.now().date().isoformat()  # noqa: DTZ005

    mood = mood or prompts.ask_rating_question("How was your mood today? (1-5)")
    productivity = productivity or prompts.ask_rating_question(
        "How was your productivity today? (1-5)"
    )
    stress = stress or prompts.ask_rating_question("How stressed were you today (1-5)?")

    try:
        database.add_daily_summary(
            database_path=database_path,
            date=date,
            mood=mood,
            productivity=productivity,
            stress=stress,
        )
    except sqlite3.IntegrityError:
        console.print(
            """ERROR: Invalid values were provided.

This is usually caused by your flag's values not being in the 1-5 constraint.
Please check your values and try again.""",
            style="red",
        )


@app.command("activity")
def add_activity(
    context: typer.Context,
    edit: Annotated[
        int | None,
        typer.Option(
            "--edit", "-e", help="The record's Activity ID that you want to update."
        ),
    ] = None,
    activity_category_input: Annotated[
        str | None,
        typer.Option("--category", "-ac", help="The activity you did today."),
    ] = None,
    activity_description_input: Annotated[
        str | None,
        typer.Option("--description", "-ad", help="The activity you did today."),
    ] = None,
    activity_start_input: Annotated[
        str | None,
        typer.Option(
            "--start",
            "-as",  # stands for activity-start
            help="The time you started the activity (HH:MM, 24-hour format).",
        ),
    ] = None,
    activity_end_input: Annotated[
        str | None,
        typer.Option(
            "--end",
            "-ae",  # stands for activity-end
            help="The time you ended the activity (HH:MM, 24-hour format).",
        ),
    ] = None,
    effort: Annotated[
        float | None,
        typer.Option("--effort", "-ef", help="The difficulty of the activity (1-5)."),
    ] = None,
    enjoyability: Annotated[
        float | None,
        typer.Option(
            "--enjoyability", "-en", help="The enjoyability of the activity (1-5)."
        ),
    ] = None,
) -> None:
    """Record an activity entry."""
    database_path = context.obj["database_path"]

    if edit:
        try:
            database.update_activity_record(
                database_path,
                edit,
                {
                    "activity_category_input": activity_category_input,
                    "activity_description": activity_description_input,
                    "activity_start": activity_start_input,
                    "activity_end": activity_end_input,
                    "effort": effort,
                    "enjoyability": enjoyability,
                },
            )
        except ValueError as error:
            console.print(f"ERROR: {error}", style="red")
            return

        except sqlite3.IntegrityError:
            console.print(
                "ERROR: Failed to update record: Invalid values were passed to the database.",
                style="red",
            )

        return

    date = datetime.now().date().isoformat()  # noqa: DTZ005

    activity_category: const.ActivityCategory = prompts.ask_activity_category(
        "What category would this activity fit into?", activity_category_input
    )

    activity_description: str | None = prompts.ask_activity_description(
        "What would be a good description for this activity? (optional):",
        activity_description_input,
    )

    activity_start = prompts.ask_datetime_question(
        "When did your activity start? (HH:MM)", activity_start_input
    )

    activity_end: str = prompts.ask_datetime_question(
        "When did your activity end? (HH:MM)", activity_end_input
    )

    effort = effort or prompts.ask_rating_question(
        "How much effort did you think this activity required? (1-5)"
    )
    enjoyability = enjoyability or prompts.ask_rating_question(
        "How much did you enjoy this activity? (1-5)"
    )

    try:
        database.add_activity(
            database_path=database_path,
            date=date,
            activity_description=activity_description,
            activity_category=activity_category,
            activity_start=activity_start,
            activity_end=activity_end,
            effort=effort,
            enjoyability=enjoyability,
        )
    except sqlite3.IntegrityError:
        console.print(
            """ERROR: Invalid values were provided.

This is usually caused by one of your flags having an invalid value.
Please check your values and try again.""",
            style="red",
        )


@app.command("sleep")
def add_sleep(
    context: typer.Context,
    edit: Annotated[
        int | None,
        typer.Option(
            "--edit",
            "-e",
            help="The record's Sleep ID that you want to be updated.",
        ),
    ] = None,
    sleep_start_input: Annotated[
        str | None,
        typer.Option(
            "--start",
            "-ss",
            help="The time you went to sleep yesterday (HH:MM, 24-hour format).",
        ),
    ] = None,
    sleep_end_input: Annotated[
        str | None,
        typer.Option(
            "--end", "-se", help="The time you woke up today (HH:MM, 24-hour format)."
        ),
    ] = None,
    sleep_quality: Annotated[
        float | None,
        typer.Option("--quality", "-q", help="The quality of your sleep (1-5)."),
    ] = None,
) -> None:
    """Record a sleep entry."""
    database_path = context.obj["database_path"]

    today_date = datetime.now().date()  # noqa: DTZ005
    yesterday_date = today_date - timedelta(days=1)

    if edit:
        try:
            database.update_sleep_record(
                database_path,
                edit,
                {
                    "sleep_start_time": time_utils.combine_date_and_time(
                        yesterday_date, sleep_start_input
                    )
                    if sleep_start_input
                    else None,
                    "sleep_end_time": time_utils.combine_date_and_time(
                        today_date, sleep_end_input
                    )
                    if sleep_end_input
                    else None,
                    "sleep_quality": sleep_quality,
                },
            )
        except ValueError as error:
            console.print(f"ERROR: {error}", style="red")
            return

        except sqlite3.IntegrityError:
            console.print(
                "ERROR: Failed to update record: Invalid values were passed in the database.",
                style="red",
            )

        return

    start_sleep_time: str = prompts.ask_datetime_question(
        "When did you start sleeping? (HH:MM)", sleep_start_input
    )
    sleep_start_datetime = time_utils.combine_date_and_time(
        yesterday_date, start_sleep_time
    ).isoformat(timespec="minutes")

    end_sleep_time: str = prompts.ask_datetime_question(
        "When did you wake up? (HH:MM)", sleep_end_input
    )
    sleep_end_datetime = time_utils.combine_date_and_time(
        today_date, end_sleep_time
    ).isoformat(timespec="minutes")

    sleep_quality = sleep_quality or prompts.ask_rating_question(
        "How was your sleep quality? (1-5)"
    )

    try:
        database.add_sleep(
            database_path=database_path,
            sleep_start_datetime=sleep_start_datetime,
            sleep_end_datetime=sleep_end_datetime,
            sleep_quality=sleep_quality,
        )
    except sqlite3.IntegrityError:
        console.print(
            """ERROR: Invalid values were provided.

This is usually caused by one of your flags having an invalid value.
Please check your values and try again.""",
            style="red",
        )


@app.command("stats")
def show_stats(
    context: typer.Context,
    table_types: Annotated[
        list[str] | None,
        typer.Option("--table", "-t", help="The table to list"),
    ] = None,
) -> None:
    database_path = context.obj["database_path"]
    if table_types is None:
        table_types = ["summary", "activity", "sleep"]
    else:
        if any(table_type not in VALID_TABLE_TYPES for table_type in table_types):
            raise typer.BadParameter("Invalid table types.")

    for table_type in table_types:
        if table_type == "summary":
            generated_table = tables.create_table(
                database.fetch_daily_summaries_records(database_path),
                tables.SUMMARY_COLUMNS,
            )

        elif table_type == "activity":
            generated_table = tables.create_table(
                database.fetch_activities_records(database_path),
                tables.ACTIVITY_COLUMNS,
            )

        else:
            generated_table = tables.create_table(
                database.fetch_sleep_records(database_path), tables.SLEEP_COLUMNS
            )

        if generated_table is None:
            console.print(
                f"There is no data inside the {table_type} table.", style="yellow"
            )
            continue

        console.print(generated_table)


@app.command("clear")
def clear_all_data(
    context: typer.Context,
    skip_confirm: Annotated[
        bool | None, typer.Option("--skip", "-s", help="Skips the confirmation prompt.")
    ] = None,
) -> None:
    """Removes all tracking data from the database.

    Args:
        skip_confirm (bool, Optional): If this flag is invoked, it skips the confirmation prompt.
    """
    database_path = context.obj["database_path"]

    clear_data_confirm = prompts.ask_for_confirmation(
        "Are you sure you want to clear the database?", skip_confirm
    )

    if clear_data_confirm:
        database.clear_database(database_path)
        print("Successfully cleared data.")
        return

    print("Aborting clear command.")
