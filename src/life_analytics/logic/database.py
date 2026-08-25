import sqlite3
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any, Literal, cast

sql_dir: Traversable = files("life_analytics.sql")

VALID_TABLE_NAMES = Literal["daily_summaries", "activities", "sleep"]


def create_database(database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    try:
        # enable foreign keys
        connection.execute("PRAGMA foreign_keys = ON")
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
    table_name: VALID_TABLE_NAMES,
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
    table_name: VALID_TABLE_NAMES,
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
        results = connection.execute(
            f"SELECT 1 FROM {table_name} WHERE {primary_key_column} = ?", (primary_key,)
        )

        if results.fetchone() is None:
            raise ValueError("Record to update does not exist.")

        connection.execute(query, (*fields_to_update.values(), primary_key))
        connection.commit()
    finally:
        connection.close()


def update_daily_summary_record(
    database_path: Path, date: str, fields: dict[str, Any]
) -> None:
    """This updates a record in the daily_summaries table based on the date (primary key)."""
    _update_record(database_path, "daily_summaries", "summary_date", date, fields)


def update_activity_record(
    database_path: Path, activity_id: int, fields: dict[str, Any]
) -> None:
    """This updates a record in the activities table based on the activity_id (primary key)."""
    _update_record(database_path, "activities", "activity_id", activity_id, fields)


def update_sleep_record(
    database_path: Path, sleep_id: int, fields: dict[str, Any]
) -> None:
    """This updates a record in the sleep table based on the sleep_id (primary key)."""
    _update_record(database_path, "sleep", "sleep_id", sleep_id, fields)


def _fetch_table_records(
    database_path: Path, table_name: VALID_TABLE_NAMES, limit: int | None = None
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
) -> list[tuple[str, int, float, float]]:
    return _fetch_table_records(database_path, "daily_summaries", limit)


def fetch_activities_records(
    database_path: Path, limit: int | None = None
) -> list[tuple[int, str, str, str, str, str, float, float, float, float]]:
    return _fetch_table_records(database_path, "activities", limit)


def fetch_sleep_records(
    database_path: Path, limit: int | None = None
) -> list[tuple[int, str, str, float, str]]:
    return _fetch_table_records(database_path, "sleep", limit)


def fetch_sleep_record(
    database_path: Path, sleep_id: int
) -> tuple[int, str, str, float, str] | None:
    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sleep WHERE sleep_id = ?", (sleep_id,))
        return cast(tuple[int, str, str, float, str], cursor.fetchone())
    finally:
        connection.close()


def migrate_database(database_path: Path, new_database_path: Path) -> None:
    # to make sure theres no duplicated data there
    new_database_path.unlink(missing_ok=True)

    create_database(new_database_path)
    new_db_connection = sqlite3.connect(new_database_path)

    try:
        daily_summary_rows = fetch_daily_summaries_records(database_path)
        activity_rows = fetch_activities_records(database_path)
        sleep_rows = fetch_sleep_records(database_path)

        new_db_connection.executemany(
            "INSERT INTO daily_summaries VALUES (?, ?, ?, ?)", (daily_summary_rows)
        )
        new_db_connection.executemany(
            "INSERT INTO activities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (activity_rows),
        )
        new_db_connection.executemany(
            "INSERT INTO sleep VALUES (?, ?, ?, ?, ?)", (sleep_rows)
        )

        new_db_connection.commit()

    except Exception:
        new_db_connection.rollback()
        raise

    finally:
        new_db_connection.close()
