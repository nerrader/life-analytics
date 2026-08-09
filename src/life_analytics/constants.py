from pathlib import Path
from typing import Final, Literal

from platformdirs import user_data_path

DEFAULT_DATABASE_PATH: Final[Path] = (
    user_data_path("life-analytics", appauthor="nerrader") / "life.db"
)
Rating = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
