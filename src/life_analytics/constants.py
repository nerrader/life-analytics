from pathlib import Path
from typing import Final, Literal

from platformdirs import user_data_path

MAIN_DATA_DIR: Final[Path] = user_data_path("life-analytics", appauthor="nerrader")
DEFAULT_DATABASE_PATH: Final[Path] = MAIN_DATA_DIR / "life.db"
ACTIVITY_START_TEXT_PATH: Final[Path] = MAIN_DATA_DIR / "activity-start-datetime.txt"

SleepType = Literal["sleep", "nap"]
VALID_SLEEP_TYPES: Final[tuple[str, str]] = ("sleep", "nap")
