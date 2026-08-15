from pathlib import Path
from typing import Final, Literal

from platformdirs import user_data_path

DEFAULT_DATABASE_PATH: Final[Path] = (
    user_data_path("life-analytics", appauthor="nerrader") / "life.db"
)

# for static checking
ActivityCategory = Literal["DEV", "MAINT", "SOCIAL", "SPORTS", "IDLE"]

# for checking at runtime
VALID_ACTIVITY_CATEGORIES: Final[tuple[str, str, str, str, str]] = (
    "DEV",
    "MAINT",
    "SOCIAL",
    "SPORTS",
    "IDLE",
)

SleepType = Literal["sleep", "nap"]
VALID_SLEEP_TYPES: Final[tuple[str, str]] = ("sleep", "nap")
