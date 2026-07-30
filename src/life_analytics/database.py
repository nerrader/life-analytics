import sqlite3
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

sql_dir: Traversable = files("life_analytics.sql")


def create_database(database_path: Path):
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript((sql_dir / "schema.sql").read_text())


def clear_database(database_path: Path):
    with sqlite3.connect(database_path) as connection:
        connection.execute((sql_dir / "clear_database.sql").read_text())
