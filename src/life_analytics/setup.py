import sqlite3
from importlib.resources import files
from pathlib import Path


def get_schema() -> str:
    return files("life_analytics.schemas").joinpath("schema.sql").read_text()


def create_database(database_path: Path):
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(get_schema())
