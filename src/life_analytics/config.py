import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from life_analytics import constants as const


@dataclass
class Config:
    database_path: Path = const.DEFAULT_DATABASE_PATH
    activity_start_path: Path = const.ACTIVITY_START_TEXT_PATH
    force_detailed_mode: bool = False
    _valid_categories: set[str] | None = None

    @property
    def valid_categories(self) -> set[str] | None:
        return self._valid_categories

    def set_value(self, name: str, value: str) -> None:
        match name:
            case "database_path":
                self.database_path = Path(value)
            case "activity_start_path":
                self.activity_start_path = Path(value)
            case "force_detailed_mode":
                if value.lower() == "true" or value == "1":
                    self.force_detailed_mode = True
                elif value.lower() == "false" or value == "0":
                    self.force_detailed_mode = False
                else:
                    raise ValueError(
                        "Use 'false' or '0' to turn it off. Use 'true' or '1' to turn it on."
                    )
            case "valid_categories":
                raise ValueError(
                    "Use the category commands to configure valid categories."
                )
            case _:
                raise ValueError(f"Unknown config option: {name}")

    def add_valid_category(self, category: str) -> None:
        if isinstance(self._valid_categories, set):
            self._valid_categories.add(category)
            return

        self._valid_categories = {category}

    def delete_valid_category(self, category: str) -> None:
        if isinstance(self._valid_categories, set):
            self._valid_categories.remove(category)
            return

        raise ValueError("There are no valid categories yet.")

    def clear_valid_categories(self) -> None:
        self._valid_categories = None

    def get_config_stats_grid(self) -> dict[str, Any]:
        return {
            "database_path": self.database_path,
            "activity_start_path": self.activity_start_path,
            "force_detailed_mode": self.force_detailed_mode,
            "valid_categories": self.valid_categories,
        }


def save_configs(config: Config) -> None:
    data = {
        "database_path": str(config.database_path),
        "activity_start_path": str(config.activity_start_path),
        "force_detailed_mode": config.force_detailed_mode,
        "valid_categories": list(config.valid_categories)
        if config.valid_categories is not None
        else None,
    }

    with open(const.CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_configs() -> Config:
    with open(const.CONFIG_PATH, encoding="utf-8") as file:
        data = json.load(file)

    return Config(
        database_path=Path(data["database_path"]),
        activity_start_path=Path(data["activity_start_path"]),
        force_detailed_mode=data["force_detailed_mode"],
        _valid_categories=set(data["valid_categories"])
        if data["valid_categories"] is not None
        else None,
    )
