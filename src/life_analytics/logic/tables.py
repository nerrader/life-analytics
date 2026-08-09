from typing import Final

from rich.table import Table

SUMMARY_COLUMNS: Final[tuple[str, ...]] = ("Date", "Mood", "Productivity", "Stress")
ACTIVITY_COLUMNS: Final[tuple[str, ...]] = (
    "Activity ID",
    "Date",
    "Activity",
    "Activity Start",
    "Activity End",
    "Difficulty",
    "Enjoyability",
)
SLEEP_COLUMNS: Final[tuple[str, ...]] = (
    "Sleep ID",
    "Sleep Start Time",
    "Sleep End Time",
    "Sleep Quality",
)


def to_db_column_name(column_name: str) -> str:
    return column_name.lower().replace(" ", "_")


def create_table(
    data: list[tuple[str, ...]], columns: list[str] | tuple[str, ...]
) -> Table | None:
    if not data:
        return None

    table = Table()

    for column in columns:
        table.add_column(column)

    for row in data:
        table.add_row(*(str(value) for value in row))

    return table
