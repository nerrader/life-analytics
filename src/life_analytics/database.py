import sqlite3
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

    from life_analytics.constants import Rating

sql_dir: Traversable = files("life_analytics.sql")


def create_database(database_path: Path) -> None:
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
    outside_for_leisure_minutes: int,
    exercise_minutes: int,
    mood: Rating,
    productivity: Rating,
    stress: Rating,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
INSERT INTO daily_summaries 
    (date,
    outside_for_leisure_minutes,
    exercise_minutes,
    mood,
    productivity,
    stress) 
    VALUES (?, ?, ?, ?, ?, ?)""",
            (
                date,
                outside_for_leisure_minutes,
                exercise_minutes,
                mood,
                productivity,
                stress,
            ),
        )
