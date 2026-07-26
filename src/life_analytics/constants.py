from pathlib import Path

from platformdirs import user_data_path

LIFE_DATABASE_FILEPATH: Path = (
    user_data_path("life-analytics", appauthor="nerrader") / "life.db"
)
