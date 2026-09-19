import sqlite3
from collections.abc import Iterable
from dataclasses import astuple, dataclass
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

from life_analytics.constants import TableName

sql_dir: Traversable = files("life_analytics.sql")


@dataclass(frozen=True)
class SummaryRecord:
    summary_date: str
    mood: int
    productivity: int
    stress: int


@dataclass(frozen=True)
class ActivityRecord:
    id: int
    category: str
    description: str | None
    start_at: str
    end_at: str
    effort: int
    enjoyability: int
    energy_before: int
    energy_after: int


@dataclass(frozen=True)
class SleepRecord:
    id: int
    start_at: str
    end_at: str
    quality: int
    sleep_type: str


def create_database(database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript((sql_dir / "schema.sql").read_text())
    finally:
        connection.close()


def clear_database(database_path: Path) -> None:
    with sqlite3.connect(database_path) as connection:
        try:
            connection.executescript((sql_dir / "clear_database.sql").read_text())
        except sqlite3.OperationalError as error:
            connection.rollback()
            print(f"Clearing database was not successful: {error!s}")
        finally:
            connection.close()


def _add_record(
    database_path: Path,
    table_name: TableName,
    fields: dict[str, Any],
) -> None:
    connection = sqlite3.connect(database_path)

    columns = ", ".join(fields)
    placeholder_question_marks = ", ".join("?" for _ in fields)

    try:
        connection.execute(
            f"""
        INSERT INTO {table_name}
        ({columns})

        VALUES ({placeholder_question_marks})
        """,
            tuple(fields.values()),
        )
        connection.commit()
    finally:
        connection.close()


def add_daily_summary(database_path: Path, fields: dict[str, Any]) -> None:
    _add_record(database_path, "daily_summaries", fields)


def add_activity(database_path: Path, fields: dict[str, Any]) -> None:
    _add_record(database_path, "activities", fields)


def add_sleep(database_path: Path, fields: dict[str, Any]) -> None:
    _add_record(database_path, "sleep", fields)


def _update_record(
    database_path: Path,
    table_name: TableName,
    primary_key_column: str,
    primary_key: str | int,
    fields: dict[str, Any],
) -> None:
    """The helper method for all update record methods.

    Args:
        primary_key: The primary key to use to identify which record to update.
        fields: The fields of the record to update.

    Raises:
        ValueError: If there are no valid fields to update, raise this error.
    """
    fields_to_update = {field: value for field, value in fields.items() if value}

    if not fields_to_update:
        raise ValueError("There are no valid fields to update.")

    update_statements = ", ".join(f"{field} = ?" for field in fields_to_update)

    query: str = (
        f"UPDATE {table_name} SET {update_statements} WHERE {primary_key_column} = ?"
    )

    connection = sqlite3.connect(database_path)
    try:
        # this is just for the existence check
        # so it doesnt silently fail if the primary key is not given
        results = connection.execute(query, (*fields_to_update.values(), primary_key))
        if results.rowcount == 0:
            raise ValueError("There are no records to update.")
        connection.commit()
    finally:
        connection.close()


def update_daily_summary_record(
    database_path: Path, date: str, fields: dict[str, Any]
) -> None:
    """This updates a record in the daily_summaries table based on the date (primary key)."""
    _update_record(database_path, "daily_summaries", "summary_date", date, fields)


def update_activity_record(
    database_path: Path, id: int, fields: dict[str, Any]
) -> None:
    """This updates a record in the activities table based on the id (primary key)."""

    _update_record(database_path, "activities", "id", id, fields)


def update_sleep_record(database_path: Path, id: int, fields: dict[str, Any]) -> None:
    """This updates a record in the sleep table based on the id (primary key)."""
    _update_record(database_path, "sleep", "id", id, fields)


def _fetch_table_records(
    database_path: Path, table_name: TableName, limit: int | None = None
) -> list[tuple[Any, ...]]:
    query = f"SELECT * FROM {table_name} ORDER BY 1 DESC"
    params = []

    if limit is not None:
        query += " LIMIT (?)"
        params.append(limit)

    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        connection.close()


def fetch_daily_summaries_records(
    database_path: Path, limit: int | None = None
) -> list[SummaryRecord]:
    return [
        SummaryRecord(*record)
        for record in _fetch_table_records(database_path, "daily_summaries", limit)
    ]


def fetch_activities_records(
    database_path: Path, limit: int | None = None
) -> list[ActivityRecord]:
    return [
        ActivityRecord(*record)
        for record in _fetch_table_records(database_path, "activities", limit)
    ]


def fetch_sleep_records(
    database_path: Path, limit: int | None = None
) -> list[SleepRecord]:
    return [
        SleepRecord(*record)
        for record in _fetch_table_records(database_path, "sleep", limit)
    ]


def fetch_activity_record(database_path: Path, id: int) -> ActivityRecord | None:
    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM activities WHERE id = ?", (id,))
        return ActivityRecord(*cursor.fetchone())
    finally:
        connection.close()


def fetch_sleep_record(database_path: Path, id: int) -> SleepRecord | None:
    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sleep WHERE id = ?", (id,))
        return SleepRecord(*cursor.fetchone())
    finally:
        connection.close()


def records_to_tuples(
    records: Iterable[SleepRecord | ActivityRecord | SummaryRecord],
) -> list[tuple[Any, ...]]:
    return [astuple(record) for record in records]


def get_table_column_names(database_path: Path, table: TableName) -> list[str]:
    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.execute(f"PRAGMA table_info('{table}')")
        table_columns_info = cursor.fetchall()
    finally:
        connection.close()

    # column_info[1] represents the actual column name
    column_names: list[str] = [column_info[1] for column_info in table_columns_info]
    return column_names
