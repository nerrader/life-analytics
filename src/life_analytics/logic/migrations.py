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
    finally:
        connection.close()
