import sqlite3
from datetime import datetime
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from shutil import copy2

from life_analytics.utils.time_utils import normalize_datetime

MIGRATIONS_DIR: Traversable = files("life_analytics.sql.migrations")


def migrate_database(database_path: Path) -> None:
    connection = sqlite3.connect(database_path)
    try:
        with connection:
            schema_version = connection.execute("PRAGMA user_version;").fetchone()[0]
            if schema_version == 0:
                print("New schema version, upgrading database from v0 to v1.")
                make_backup(database_path)
                print(f"Made a backup at {database_path}.backup if something breaks.")
                connection.executescript((MIGRATIONS_DIR / "v0_to_v1.sql").read_text())
            update_datetimes(connection)
    finally:
        connection.close()


def make_backup(database_path: Path) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    copy2(database_path, database_path.with_suffix(f".db.{timestamp}.backup"))


def update_datetimes(connection: sqlite3.Connection) -> None:
    activities = connection.execute(
        "SELECT id, start_at, end_at FROM activities"
    ).fetchall()

    for activity_id, start_at, end_at in activities:
        connection.execute(
            """
            UPDATE activities
            SET start_at = ?, end_at = ?
            WHERE id = ?
            """,
            (
                normalize_datetime(start_at),
                normalize_datetime(end_at),
                activity_id,
            ),
        )

    # Sleep
    sleep_records = connection.execute(
        "SELECT id, start_at, end_at FROM sleep"
    ).fetchall()

    for sleep_id, start_at, end_at in sleep_records:
        connection.execute(
            """
            UPDATE sleep
            SET start_at = ?, end_at = ?
            WHERE id = ?
            """,
            (
                normalize_datetime(start_at),
                normalize_datetime(end_at),
                sleep_id,
            ),
        )
