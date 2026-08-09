import sqlite3

# from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

    from life_analytics.constants import Rating

sql_dir: Traversable = files("life_analytics.sql")


# @dataclass(frozen=True)
# class DailySummaryRecord:
#     date: str
#     mood: int
#     productivity: int
#     stress: int
#
#
# @dataclass(frozen=True)
# class ActivityRecord:
#     activity_id: int
#     date: str
#     activity: str
#     activity_start: str
#     activity_end: str
#     difficulty: int
#     enjoyability: int
#
#
# @dataclass(frozen=True)
# class SleepRecord:
#     sleep_id: int
#     sleep_start_time: str
#     sleep_end_time: str
#     sleep_quality: int


def create_database(database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript((sql_dir / "schema.sql").read_text())


def clear_database(database_path: Path) -> None:
    with sqlite3.connect(database_path) as connection:
        try:
            connection.executescript((sql_dir / "clear_database.sql").read_text())
        except sqlite3.OperationalError as error:
            print(f"Clearing database was not successful: {error!s}")


def add_daily_summary(
    database_path: Path,
    date: str,
    mood: Rating,
    productivity: Rating,
    stress: Rating,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
INSERT INTO daily_summaries
    (date,
    mood,
    productivity,
    stress)
    VALUES (?, ?, ?, ?)""",
            (
                date,
                mood,
                productivity,
                stress,
            ),
        )


def add_activity(
    database_path: Path,
    date: str,
    activity: str,
    activity_start: str,
    activity_end: str,
    difficulty: Rating,
    enjoyability: Rating,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
INSERT INTO activities
    (date,
    activity,
    activity_start,
    activity_end,
    difficulty,
    enjoyability)
    VALUES (?, ?, ?, ?, ?, ?)""",
            (
                date,
                activity,
                activity_start,
                activity_end,
                difficulty,
                enjoyability,
            ),
        )


def add_sleep(
    database_path: Path,
    sleep_start_datetime: str,
    sleep_end_datetime: str,
    sleep_quality: Rating,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
    sleep_end_time,
    sleep_quality)
    VALUES (?, ?, ?)""",
            (
                sleep_start_datetime,
                sleep_end_datetime,
                sleep_quality,
            ),
        )


def _update_record(
    database_path: Path,
    table_name: str,
    primary_key_column: str,
    primary_key: str | int,
    fields: dict[str, Any],
):
    validated_fields = {field: value for field, value in fields.items() if value}
    if not validated_fields:
        raise ValueError("There are no valid fields to update.")

    update_statements = ", ".join(f"{field} = ?" for field in validated_fields)

    query: str = (
        f"UPDATE {table_name} SET {update_statements} WHERE {primary_key_column} = ?"
    )

    with sqlite3.connect(database_path) as connection:
        connection.execute(query, (*validated_fields.values(), primary_key))


def update_daily_summary_record(database_path: Path, date: str, fields: dict[str, Any]):
    """This updates a record in the daily_summaries table based on the date (primary key).

    Args:
        date: The date of the daily summary record you want to update.
        fields: The fields that you want to update in the record.

    Raises:
        ValueError: If there are no valid fields to update.
    """
    _update_record(database_path, "daily_summaries", "date", date, fields)


def update_activity_record(
    database_path: Path, activity_id: int, fields: dict[str, Any]
):
    _update_record(database_path, "activities", "activity_id", activity_id, fields)


def update_sleep_record(database_path: Path, sleep_id: int, fields: dict[str, Any]):
    _update_record(database_path, "sleep", "sleep_id", sleep_id, fields)


def fetch_daily_summaries_records(
    database_path: Path, limit: int | None = None
) -> list[tuple]:
    query = "SELECT * FROM daily_summaries ORDER BY date DESC"
    params = []

    if limit is not None:
        query += "LIMIT (?)"
        params.append(limit)

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def fetch_activities_records(
    database_path: Path, limit: int | None = None
) -> list[tuple]:

    query = "SELECT * FROM activities ORDER BY activity_id DESC"
    params = []

    if limit is not None:
        query += "LIMIT (?)"
        params.append(limit)

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def fetch_sleep_records(database_path: Path, limit: int | None = None) -> list[tuple]:
    query = "SELECT * FROM sleep ORDER BY sleep_id DESC"
    params = []

    if limit is not None:
        query += "LIMIT (?)"
        params.append(limit)

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
