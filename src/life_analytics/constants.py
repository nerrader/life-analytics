from pathlib import Path
from typing import Final

from platformdirs import user_data_path

DEFAULT_DATABASE_PATH: Final[Path] = (
    user_data_path("life-analytics", appauthor="nerrader") / "life.db"
)
