import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Final

import typer
from rich.console import Console

from life_analytics import __version__, config
from life_analytics.domain import constants as const
from life_analytics.domain import errors, validation
from life_analytics.logic import (
    database,
    display,
    migrations,
    prompts,
    stats,
)
from life_analytics.utils import time_utils

app = typer.Typer()
config_app = typer.Typer(help="A subcommand to manage configs")
categories_app = typer.Typer(help="A subcommand to manage valid_categories.")

app.add_typer(config_app, name="config")
config_app.add_typer(categories_app, name="category")

console = Console()

VALID_TABLE_TYPES: Final[tuple[str, ...]] = ("summary", "activity", "sleep")


def get_user_commands() -> str:
    return " ".join(sys.argv[1:])


def validate_input_category(
    short_flag: str,
    long_flag: str,
    value: str | None,
    valid_categories: set[str] | None,
) -> bool:
    if (
        value is not None
        and validation.is_valid_category(value, valid_categories) is False
    ):
        user_commands = get_user_commands()

        source_highlight = f"--{long_flag} {value}"
        if source_highlight not in user_commands:
            source_highlight = f"-{short_flag} {value}"

        if valid_categories is not None and value not in valid_categories:
            display.display_error(
                errors.ErrorDiagnostic(
                    message=f"category not in valid categories: {value}",
                    help=f"use `config list` to view current categories, or use `config category add` to add {value} as category",
                    source=user_commands,
                    source_highlight=source_highlight,
                )
            )
        else:
            display.display_error(
                errors.ErrorDiagnostic(
                    message=f"category cannot be blank: '{value}'",
                    source=user_commands,
                    source_highlight=source_highlight,
                )
            )

        return False
    return True


def validate_input_rating(short_flag: str, long_flag: str, value: float | None) -> bool:
    if value is not None and not validation.is_valid_rating(value):
        user_commands = get_user_commands()

        source_highlight = f"--{long_flag} {value!s}"
        if source_highlight not in user_commands:
            source_highlight = f"-{short_flag} {value}"

        display.display_error(
            errors.ErrorDiagnostic(
                message=f"inputted rating is not valid: {value}.",
                source=user_commands,
                source_highlight=source_highlight,
                help="change value value to be 1-5.",
            )
        )
        return False
    return True


def validate_input_datetime(short_flag: str, long_flag: str, value: str | None) -> bool:
    if value is not None and not validation.is_valid_datetime(value):
        user_commands = get_user_commands()

        source_highlight = f"--{long_flag} {value!s}"
        if source_highlight not in user_commands:
            source_highlight = f"-{short_flag} {value}"

        display.display_error(
            errors.ErrorDiagnostic(
                message=f"inputted datetime is not valid: {value}.",
                source=user_commands,
                source_highlight=source_highlight,
                help="ensure value follows the YYYY-MM-DD HH:MM format",
            )
        )
        return False
    return True


def validate_input_time(short_flag: str, long_flag: str, value: str | None) -> bool:
    if value is not None and not validation.is_valid_time(value):
        user_commands = get_user_commands()

        source_highlight = f"--{long_flag} {value!s}"
        if source_highlight not in user_commands:
            source_highlight = f"-{short_flag} {value}"

        display.display_error(
            errors.ErrorDiagnostic(
                message=f"inputted time is not valid: {value}.",
                source=user_commands,
                source_highlight=source_highlight,
                help="ensure value follows the HH:MM format",
            )
        )
        return False
    return True


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    database_path: Annotated[
        Path | None,
        typer.Option(
            "--database-path",
            "-db",
            help="Path to the database file.",
        ),
    ] = None,
    activity_start_path: Annotated[
        Path | None,
        typer.Option(
            "--activity-start-path",
            "-ap",
            help="This is the path used for the start and stop text file storage.",
        ),
    ] = None,
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Displays the version")
    ] = False,
) -> None:
    """For more information on advanced usage, like using command options and editing,
    refer to the 'How to Use' section in the life analytics GitHub README."""
    # this is so every command function can access the db path
    try:
        configuration = config.load_configs()
    except FileNotFoundError:
        configuration = config.Config()

    if database_path is not None:
        configuration.database_path = database_path
    if activity_start_path is not None:
        configuration.activity_start_path = activity_start_path

    context.obj = {"config": configuration}

    if version:
        print(__version__)
        return

    if not configuration.database_path.exists():
        database.create_database(configuration.database_path)
    else:
        migrations.migrate_database(configuration.database_path)


@app.command("summary")
def add_daily_summary(
    context: typer.Context,
    edit: Annotated[
        str | None,
        typer.Option(
            "--edit",
            help="The record's date to edit (YYYY-MM-DD). Use the flags/options to update the specific fields. Interactive mode cannot be used when editing.",
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
        typer.Option("--stress", "-s", help="Your stress levels today (1-5)."),
    ] = None,
) -> None:
    """Record a daily summary entry. Omitting the *optional* flags will trigger interactive mode."""
    configuration: config.Config = context.obj["config"]
    database_path = configuration.database_path

    if edit:
        validate_input_rating("m", "mood", mood)
        validate_input_rating("p", "productivity", productivity)
        validate_input_rating("s", "stress", stress)
        try:
            database.update_daily_summary_record(
                database_path,
                edit,
                {"mood": mood, "productivity": productivity, "stress": stress},
            )
        except errors.NoUpdateFieldsError as error:
            new_diagnostics = errors.ErrorDiagnostic(
                message=error.diagnostic.message, help="check your command options"
            )
            display.display_error(new_diagnostics)
        except errors.NoUpdateRecordsError as error:
            new_diagnostics = errors.ErrorDiagnostic(
                message=error.diagnostic.message,
                help="check if --edit ID is an existing ID.",
                source=" ".join(sys.argv[1:]),
            )
            display.display_error(new_diagnostics)
            return

        except sqlite3.IntegrityError as error:
            console.print(
                f"""ERROR: Failed to update record: Invalid values were passed to the database.

Full Error Message:
{error}"""
            )
        return

    date = datetime.now().date().isoformat()

    mood = mood or prompts.ask_rating_question("How was your mood today? (1-5)")
    productivity = productivity or prompts.ask_rating_question(
        "How was your productivity today? (1-5)"
    )
    stress = stress or prompts.ask_rating_question("How stressed were you today (1-5)?")

    try:
        database.add_daily_summary(
            database_path,
            {
                "summary_date": date,
                "mood": mood,
                "productivity": productivity,
                "stress": stress,
            },
        )
    except sqlite3.IntegrityError as error:
        console.print(
            f"""ERROR: Invalid values were provided.

This is usually caused by your flag's values not being in the 1-5 constraint.
Please check your values and try again.

Full Error Message: {error}""",
            style="red",
        )


@app.command("activity")
def add_activity(
    context: typer.Context,
    edit: Annotated[
        int | None,
        typer.Option(
            "--edit",
            help="The record's ID to edit. Use the flags/options to update the specific fields. Interactive mode cannot be used when editing.",
        ),
    ] = None,
    detailed: Annotated[
        bool,
        typer.Option(
            "--detailed",
            help="If this flag is provoked, require explicit dates.",
        ),
    ] = False,
    category_input: Annotated[
        str | None,
        typer.Option(
            "--category",
            "-c",
            help="The category of the activity you did today. Available categories are: 'IDLE', 'MAINT', 'DEV', 'SCHOOL', 'SPORTS', 'SOCIAL'.",
        ),
    ] = None,
    description_input: Annotated[
        str | None,
        typer.Option("--description", "-d", help="Further describe your activity."),
    ] = None,
    activity_start_input: Annotated[
        str | None,
        typer.Option(
            "--start",
            "-s",  # stands for activity-start
            help="The time you started the activity (HH:MM, 24-hour format).",
        ),
    ] = None,
    activity_end_input: Annotated[
        str | None,
        typer.Option(
            "--end",
            "-e",  # stands for activity-end
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
    energy_before: Annotated[
        float | None,
        typer.Option(
            "--energy-before", "-eb", help="Your energy before the activity (1-5)."
        ),
    ] = None,
    energy_after: Annotated[
        float | None,
        typer.Option(
            "--energy-after", "-ea", help="Your energy after the activity (1-5)."
        ),
    ] = None,
) -> None:
    """Record an activity entry. Omitting the *optional* flags will trigger interactive mode."""
    configuration: config.Config = context.obj["config"]
    database_path = configuration.database_path

    if configuration.force_detailed_mode:
        detailed = True

    if (
        validate_input_category(
            "c", "category", category_input, configuration.valid_categories
        )
        is False
    ):
        return

    if validate_input_rating("ef", "effort", effort) is False:
        return

    if validate_input_rating("en", "enjoyability", enjoyability) is False:
        return

    if validate_input_rating("eb", "energy_before", energy_before) is False:
        return

    if validate_input_rating("ea", "energy_after", energy_after) is False:
        return

    if detailed:
        if validate_input_datetime("s", "start", activity_start_input) is False:
            return
        if validate_input_datetime("e", "end", activity_end_input) is False:
            return
    else:
        if validate_input_time("s", "start", activity_start_input) is False:
            return
        if validate_input_time("e", "end", activity_end_input) is False:
            return

    if edit:
        try:
            edit_record = database.fetch_activity_record(database_path, edit)
            if edit_record is None:
                display.display_error(
                    errors.ErrorDiagnostic(
                        message="--edit gave a non-existant record.",
                        help="use `list` to find record IDs",
                    )
                )
                return

            if detailed:
                start_datetime = (
                    time_utils.datetime_string_to_iso(activity_start_input)
                    if activity_start_input is not None
                    else None
                )

                end_datetime = (
                    time_utils.datetime_string_to_iso(activity_end_input)
                    if activity_end_input is not None
                    else None
                )
            else:
                existing_start_date = datetime.fromisoformat(
                    edit_record.start_at
                ).date()
                existing_end_date = datetime.fromisoformat(edit_record.end_at).date()

                start_datetime = (
                    time_utils.combine_date_and_time(
                        existing_start_date, activity_start_input
                    ).isoformat(timespec="minutes")
                    if activity_start_input
                    else None
                )

                end_datetime = (
                    time_utils.combine_date_and_time(
                        existing_end_date, activity_end_input
                    ).isoformat(timespec="minutes")
                    if activity_end_input
                    else None
                )

            database.update_activity_record(
                database_path,
                edit,
                {
                    "category": category_input,
                    "description": description_input,
                    "start_at": start_datetime,
                    "end_at": end_datetime,
                    "effort": effort,
                    "enjoyability": enjoyability,
                    "energy_before": energy_before,
                    "energy_after": energy_after,
                },
            )
        except errors.NoUpdateFieldsError as error:
            new_diagnostics = errors.ErrorDiagnostic(
                message=error.diagnostic.message, help="check your command options"
            )
            display.display_error(new_diagnostics)

        except errors.NoUpdateRecordsError as error:
            new_diagnostics = errors.ErrorDiagnostic(
                message=error.diagnostic.message,
                help="check if --edit ID is an existing ID.",
                source=get_user_commands(),
            )
            display.display_error(new_diagnostics)
            return

        except sqlite3.IntegrityError as error:
            console.print(
                f"""ERROR: Failed to update record: Invalid values were passed to the database.

    Full Error Message:
    {error}""",
                style="red",
            )

        return

    date = datetime.now().date().isoformat()
    current_time = (
        datetime.now().time().isoformat(timespec="minutes")
    )  # for activity end default

    activity_category: str = prompts.ask_activity_category(
        "What category would this activity fit into?",
        configuration.valid_categories,
        category_input,
    )

    activity_description: str | None = prompts.ask_activity_description(
        "What would be a good description for this activity? (optional):",
        description_input,
    )

    if detailed:
        activity_start = prompts.ask_datetime_question(
            "When did your activity start? (YYYY-MM-DD HH:MM)", activity_start_input
        )
        activity_end = prompts.ask_datetime_question(
            "When did your activity end? (YYYY-MM-DD HH:MM)", activity_end_input
        )
    else:
        activity_start = prompts.ask_time_question(
            "When did your activity start? (HH:MM)", activity_start_input
        )
        activity_start = f"{date}T{activity_start}"

        activity_end = prompts.ask_time_question(
            "When did your activity end? (HH:MM)",
            activity_end_input,
            default=current_time,
        )
        activity_end = f"{date}T{activity_end}"

    effort = effort or prompts.ask_rating_question(
        "How much effort did you think this activity required? (1-5)"
    )

    enjoyability = enjoyability or prompts.ask_rating_question(
        "How much did you enjoy this activity? (1-5)"
    )

    energy_before = energy_before or prompts.ask_rating_question(
        "How much energy did you have before your activity? (1-5)"
    )

    energy_after = energy_after or prompts.ask_rating_question(
        "How much energy did you have after your activity? (1-5)"
    )

    try:
        database.add_activity(
            database_path,
            {
                "category": activity_category,
                "description": activity_description,
                "start_at": activity_start,
                "end_at": activity_end,
                "effort": effort,
                "enjoyability": enjoyability,
                "energy_before": energy_before,
                "energy_after": energy_after,
            },
        )
    except sqlite3.IntegrityError as error:
        console.print(
            f"""ERROR: Invalid values were provided.

This is usually caused by one of your flags having an invalid value.
Please check your values and try again.

Full Error Message:
{error}""",
            style="red",
        )


@app.command("sleep")
def add_sleep(
    context: typer.Context,
    edit: Annotated[
        int | None,
        typer.Option(
            "--edit",
            help="The record's ID to edit. Use the flags/options to update the specific fields. Interactive mode cannot be used when editing.",
        ),
    ] = None,
    sleep_type: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The sleep type: 'sleep' or 'nap'. When creating a nap, both start and end dates default to today.",
        ),
    ] = "sleep",
    detailed: Annotated[
        bool,
        typer.Option(
            "--detailed",
            help="If this flag is provoked, require explicit dates.",
        ),
    ] = False,
    sleep_start_input: Annotated[
        str | None,
        typer.Option(
            "--start",
            "-s",
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
        float | None,
        typer.Option("--quality", "-q", help="The quality of your sleep (1-5)."),
    ] = None,
) -> None:
    """Record a sleep entry. Omitting the *optional* flags will trigger interactive mode."""
    configuration: config.Config = context.obj["config"]
    database_path = configuration.database_path

    if configuration.force_detailed_mode:
        detailed = True

    today_date = datetime.now().date()
    yesterday_date = today_date - timedelta(days=1)

    if detailed:
        if validate_input_datetime("s", "start", sleep_start_input) is False:
            return
        if validate_input_datetime("e", "end", sleep_end_input) is False:
            return
    else:
        if validate_input_time("s", "start", sleep_start_input) is False:
            return
        if validate_input_time("e", "end", sleep_end_input) is False:
            return

    if validate_input_rating("q", "quality", sleep_quality) is False:
        return

    if sleep_type is not None and sleep_type not in ["sleep", "nap"]:
        user_commands = get_user_commands()
        source_highlight = f"--type {sleep_type}"
        if source_highlight not in user_commands:
            source_highlight = f"-t {sleep_type}"

        display.display_error(
            errors.ErrorDiagnostic(
                message=f"invalid sleep_type value: {sleep_type}",
                source=user_commands,
                source_highlight=source_highlight,
                help="use 'sleep' or 'nap' for sleep_type.",
            )
        )
        return

    if edit:
        try:
            edit_sleep_record = database.fetch_sleep_record(database_path, edit)
            if edit_sleep_record is None:
                display.display_error(
                    errors.ErrorDiagnostic(
                        message="--edit gave a non-existant record.",
                        help="use `list` to find record IDS.",
                    )
                )
                return

            if not detailed:
                sleep_start_date = datetime.fromisoformat(
                    edit_sleep_record.start_at
                ).date()
                sleep_end_date = datetime.fromisoformat(edit_sleep_record.end_at).date()

                start_datetime = (
                    time_utils.combine_date_and_time(
                        sleep_start_date, sleep_start_input
                    ).isoformat(timespec="minutes")
                    if sleep_start_input
                    else None
                )
                end_datetime = (
                    time_utils.combine_date_and_time(
                        sleep_end_date, sleep_end_input
                    ).isoformat(timespec="minutes")
                    if sleep_end_input
                    else None
                )
            else:
                start_datetime = (
                    time_utils.datetime_string_to_iso(sleep_start_input)
                    if sleep_start_input is not None
                    else None
                )

                end_datetime = (
                    time_utils.datetime_string_to_iso(sleep_end_input)
                    if sleep_end_input is not None
                    else None
                )

            database.update_sleep_record(
                database_path,
                edit,
                {
                    "start_at": start_datetime,
                    "end_at": end_datetime,
                    "quality": sleep_quality,
                    "sleep_type": sleep_type,
                },
            )
        except errors.NoUpdateFieldsError as error:
            new_diagnostics = errors.ErrorDiagnostic(
                message=error.diagnostic.message, help="check your command options"
            )
            display.display_error(new_diagnostics)
        except errors.NoUpdateRecordsError as error:
            new_diagnostics = errors.ErrorDiagnostic(
                message=error.diagnostic.message,
                help="check if --edit ID is an existing ID.",
                source=get_user_commands(),
            )
            display.display_error(new_diagnostics)
            return

        except sqlite3.IntegrityError as error:
            console.print(
                f"""ERROR: Failed to update record: Invalid values were passed in the database.

Full Error Message:
{error}""",
                style="red",
            )

        return

    if detailed:
        sleep_start_datetime: str = prompts.ask_datetime_question(
            "When did you start sleeping (YYYY-MM-DD HH:MM)?", sleep_start_input
        )
        sleep_end_datetime: str = prompts.ask_datetime_question(
            "When did you wake up (YYYY-MM-DD HH:MM)?", sleep_end_input
        )

    else:
        start_sleep_time: str = prompts.ask_time_question(
            "When did you start sleeping? (HH:MM)", sleep_start_input
        )

        sleep_start_datetime = time_utils.combine_date_and_time(
            today_date if sleep_type == "nap" else yesterday_date, start_sleep_time
        ).isoformat(timespec="minutes")

        end_sleep_time: str = prompts.ask_time_question(
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
            database_path,
            {
                "start_at": sleep_start_datetime,
                "end_at": sleep_end_datetime,
                "quality": sleep_quality,
                "sleep_type": sleep_type,
            },
        )
    except sqlite3.IntegrityError as error:
        console.print(
            f"""ERROR: Invalid values were provided.

This is usually caused by one of your flags having an invalid value.
Please check your values and try again.

Full Error Message:
{error}""",
            style="red",
        )


@app.command("ls", hidden=True)
@app.command("list")
def list_records(
    context: typer.Context,
    table_types: Annotated[
        list[str] | None,
        typer.Option(
            "--table",
            "-t",
            help="The table to list. Available options are: 'summary', 'activity', 'sleep'.",
        ),
    ] = None,
    limit: Annotated[
        int | None,
        typer.Option("--limit", "-l", help="The limit of rows to fetch"),
    ] = None,
) -> None:
    """Display all-time daily summaries, activities, and sleep. Aliases: 'ls'"""
    configuration = context.obj["config"]
    database_path = configuration.database_path

    if table_types is None:
        table_types = ["summary", "activity", "sleep"]
    else:
        if any(table_type not in VALID_TABLE_TYPES for table_type in table_types):
            raise typer.BadParameter("Invalid table types.")

    table_name_map: dict[str, const.TableName] = {
        "summary": "daily_summaries",
        "activity": "activities",
        "sleep": "sleep",
    }

    for table_type in table_types:
        table_type = table_name_map[table_type]

        display_columns = [
            display.db_to_table_column_name(column_name)
            for column_name in database.get_table_column_names(
                database_path, table_type
            )
        ]

        if table_type == "daily_summaries":
            generated_table = display.create_table(
                database.records_to_tuples(
                    database.fetch_daily_summaries_records(database_path, limit)
                ),
                display_columns,
            )

        elif table_type == "activities":
            generated_table = display.create_table(
                database.records_to_tuples(
                    database.fetch_activities_records(database_path, limit)
                ),
                display_columns,
            )

        else:
            generated_table = display.create_table(
                database.records_to_tuples(
                    database.fetch_sleep_records(database_path, limit)
                ),
                display_columns,
            )

        if generated_table is None:
            console.print(
                f"There is no data inside the {table_type} table.", style="yellow"
            )
            continue

        console.print(generated_table)


@app.command("stats")
def display_stats(context: typer.Context) -> None:
    """Displays overall statistics of collected data"""
    configuration = context.obj["config"]
    database_path = configuration.database_path

    summary_records = database.fetch_daily_summaries_records(database_path)
    activity_records = database.fetch_activities_records(database_path)
    sleep_records = database.fetch_sleep_records(database_path)

    tracking_data = stats.calculate_tracking_stats(summary_records)
    summary_data = stats.calculate_daily_summary_data(summary_records)
    activity_data = stats.calculate_activity_data(activity_records)
    sleep_data = stats.calculate_sleep_data(sleep_records)

    average_duration_format = "{}h {}m"
    # tryna do some formatting here
    activity_average_duration = activity_data["Avg Duration"]
    hours, minutes = divmod(round(activity_average_duration / 60), 60)
    activity_data["Avg Duration"] = average_duration_format.format(hours, minutes)

    sleep_average_duration = sleep_data["Avg Duration"]
    hours, minutes = divmod(round(sleep_average_duration / 60), 60)
    sleep_data["Avg Duration"] = average_duration_format.format(hours, minutes)

    stat_dict = tracking_data.copy()
    stat_dict["Daily Summaries"] = summary_data
    stat_dict["Activities"] = activity_data
    stat_dict["Sleep"] = sleep_data

    grid = display.create_stats_grid(stat_dict)
    console.print(grid)


@app.command("clear")
def clear_all_data(
    context: typer.Context,
    skip_confirm: Annotated[
        bool | None, typer.Option("--skip", "-s", help="Skips the confirmation prompt.")
    ] = None,
) -> None:
    """Removes all tracking data from the database."""
    configuration = context.obj["config"]
    database_path = configuration.database_path

    clear_data_confirm = prompts.ask_for_confirmation(
        "Are you sure you want to clear the database?", skip_confirm
    )

    if clear_data_confirm:
        database.clear_database(database_path)
        print("Successfully cleared data.")
        return

    print("Aborting clear command.")


@app.command("start")
def start_activity_time(context: typer.Context) -> None:
    """Start tracking an activity"""
    activity_start_path: Path = context.obj["activity_start_path"]

    if activity_start_path.exists():
        confirm = prompts.ask_for_confirmation(
            "Are you sure you want to rewrite the existing started activity?"
        )
        if not confirm:
            return

    date_time: str = datetime.now().isoformat(timespec="minutes")
    print(f"Activity started: {date_time.replace('T', ' ')}")

    activity_start_path.write_text(date_time)


@app.command("end")
def end_activity_time(
    context: typer.Context,
    category_input: Annotated[
        str | None,
        typer.Option(
            "--category",
            "-c",
            help="The category of the activity you did today. Available categories are: 'IDLE', 'MAINT', 'DEV', 'SCHOOL', 'SPORTS', 'SOCIAL'.",
        ),
    ] = None,
    description_input: Annotated[
        str | None,
        typer.Option("--description", "-d", help="Further describe your activity."),
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
    energy_before: Annotated[
        float | None,
        typer.Option(
            "--energy-before", "-eb", help="Your energy before the activity (1-5)."
        ),
    ] = None,
    energy_after: Annotated[
        float | None,
        typer.Option(
            "--energy-after", "-ea", help="Your energy after the activity (1-5)."
        ),
    ] = None,
) -> None:
    """Stops the activity tracking, and prompts for activity details."""
    configuration = context.obj["config"]
    database_path = configuration.database_path
    activity_start_path = configuration.activity_start_path

    if not activity_start_path.exists():
        display.display_error(
            errors.ErrorDiagnostic(
                message="started activity not found.",
                help="use `start` to start an activity first.",
            )
        )
        return

    if (
        validate_input_category(
            "c", "category", category_input, configuration.valid_categories
        )
        is False
    ):
        return

    if validate_input_rating("ef", "effort", effort) is False:
        return

    if validate_input_rating("en", "enjoyability", enjoyability) is False:
        return

    if validate_input_rating("eb", "energy_before", energy_before) is False:
        return

    if validate_input_rating("ea", "energy_after", energy_after) is False:
        return

    start_activity_datetime = activity_start_path.read_text()
    end_activity_datetime = datetime.now().isoformat(timespec="minutes")

    activity_start_path.unlink()

    activity_category: str = prompts.ask_activity_category(
        "What category would this activity fit into?",
        configuration.valid_categories,
        category_input,
    )

    activity_description: str | None = prompts.ask_activity_description(
        "What would be a good description for this activity? (optional):",
        description_input,
    )

    effort = effort or prompts.ask_rating_question(
        "How much effort did you think this activity required? (1-5)"
    )

    enjoyability = enjoyability or prompts.ask_rating_question(
        "How much did you enjoy this activity? (1-5)"
    )

    energy_before = energy_before or prompts.ask_rating_question(
        "How much energy did you have before your activity? (1-5)"
    )

    energy_after = energy_after or prompts.ask_rating_question(
        "How much energy did you have after your activity? (1-5)"
    )
    database.add_activity(
        database_path,
        {
            "category": activity_category,
            "description": activity_description,
            "start_at": start_activity_datetime,
            "end_at": end_activity_datetime,
            "effort": effort,
            "enjoyability": enjoyability,
            "energy_before": energy_before,
            "energy_after": energy_after,
        },
    )


@config_app.command("set")
def set_config(
    context: typer.Context,
    name: Annotated[str, typer.Argument(help="The name of the config.")],
    value: Annotated[str, typer.Argument(help="The value of the config.")],
) -> None:
    """Sets the config value for the name of the config."""
    configuration: config.Config = context.obj["config"]
    try:
        configuration.set_value(name, value)
        config.save_configs(configuration)
    except errors.InvalidForceDetailModeConfigError as error:
        new_diagnostics = errors.ErrorDiagnostic(
            message=error.diagnostic.message,
            source=" ".join(sys.argv[:1]),
            source_highlight=error.diagnostic.source_highlight,
            help=error.diagnostic.help,
        )
        display.display_error(new_diagnostics)
    except errors.InvalidConfigNameError as error:
        new_diagnostics = errors.ErrorDiagnostic(
            message=error.diagnostic.message,
            source=get_user_commands(),
            source_highlight=error.diagnostic.source_highlight,
            help="use `config list` to display available config names.",
        )
        display.display_error(new_diagnostics)
    except errors.ValidCategoriesNotSettableError as error:
        new_diagnostics = errors.ErrorDiagnostic(
            message=error.diagnostic.message,
            source=get_user_commands(),
            source_highlight=error.diagnostic.source_highlight,
            help="use `config category` instead.",
        )
        display.display_error(new_diagnostics)


@config_app.command("ls", hidden=True)
@config_app.command("list")
def display_configs(context: typer.Context) -> None:
    """Displays configs. Aliases: 'ls'"""
    configuration: config.Config = context.obj["config"]
    config_stats_grid_data = configuration.get_config_stats_grid()

    console.print(display.create_stats_grid(config_stats_grid_data))


@config_app.command("defaults")
def config_set_defaults(
    context: typer.Context,
    skip_confirm: Annotated[
        bool | None,
        typer.Option("--skip", "-s", help="To skip the confirmation prompt"),
    ] = None,
) -> None:
    """Clears the categories in valid_categories."""
    configuration: config.Config = context.obj["config"]

    confirmation = prompts.ask_for_confirmation(
        "Are you sure you want to set the configs to default?", skip_confirm
    )
    if confirmation:
        configuration = config.Config()
        config.save_configs(configuration)


@categories_app.command("add")
def add_category(
    context: typer.Context,
    category_name: Annotated[str, typer.Argument(help="The category to add")],
) -> None:
    """Adds a category to the valid_categories config."""
    configuration: config.Config = context.obj["config"]
    configuration.add_valid_category(category_name)
    config.save_configs(configuration)


@categories_app.command("del", hidden=True)
@categories_app.command("rm", hidden=True)
@categories_app.command("remove", hidden=True)
@categories_app.command("delete")
def delete_category(
    context: typer.Context,
    category: Annotated[str, typer.Argument(help="The category to delete.")],
) -> None:
    """Deletes a category to the valid_categories config. Aliases: 'remove', 'delete', 'del', 'rm'"""
    configuration: config.Config = context.obj["config"]
    try:
        configuration.delete_valid_category(category)
        config.save_configs(configuration)

    except errors.NoCategoriesError as error:
        display.display_error(errors.ErrorDiagnostic(message=error.diagnostic.message))

    except errors.CategoryNotFoundError as error:
        display.display_error(
            errors.ErrorDiagnostic(
                message=error.diagnostic.message,
                source=get_user_commands(),
                source_highlight=error.diagnostic.source_highlight,
            )
        )


@categories_app.command("clear")
def clear_category(
    context: typer.Context,
    skip_confirm: Annotated[
        bool | None,
        typer.Option("--skip", "-s", help="To skip the confirmation prompt"),
    ] = None,
) -> None:
    """Clears the categories in valid_categories."""
    configuration: config.Config = context.obj["config"]

    confirmation = prompts.ask_for_confirmation(
        "Are you sure you want to clear the valid categories?", skip_confirm
    )
    if confirmation:
        configuration.clear_valid_categories()
        config.save_configs(configuration)
