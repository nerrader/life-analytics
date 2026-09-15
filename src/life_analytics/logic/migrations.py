import sqlite3
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path

MIGRATIONS_DIR: Traversable = files("life_analytics.sql.migrations")


def migrate_database(database_path: Path) -> None:
    connection = sqlite3.connect(database_path)
    try:
        with connection:
            schema_version = connection.execute("PRAGMA user_version;").fetchone()[0]
            if schema_version == 0:
                print("New schema version, upgrading database from v0 to v1.")
                connection.executescript((MIGRATIONS_DIR / "v0_to_v1.sql").read_text())
            update_datetimes(connection)
    finally:
        connection.close()


def update_datetimes(connection: sqlite3.Connection) -> None:
    def normalize_datetime(isostring: str) -> str:
        """This makes sure the time part of the datetime isostring is valid.
        Example: 2026-12-25T6:30 -> 2026-12-25T06:30"""
        date, time = isostring.split("T", 1)
        hour, minutes = time.split(":", 1)

        return f"{date}T{hour.zfill(2)}:{minutes}"

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
