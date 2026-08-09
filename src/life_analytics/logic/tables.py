from typing import Final

from rich.table import Table

SUMMARY_COLUMNS: Final[tuple] = ("Date", "Mood", "Productivity", "Stress")
ACTIVITY_COLUMNS: Final[tuple] = (
    "Activity ID",
    "Date",
    "Activity",
    "Activity Start",
    "Activity End",
    "Difficulty",
    "Enjoyability",
)
SLEEP_COLUMNS: Final[tuple] = (
    "Sleep ID",
    "Sleep Start Time",
    "Sleep End Time",
    "Sleep Quality",
)


def to_db_column_name(column_name: str) -> str:
    return column_name.lower().replace(" ", "_")


def create_table(data: list[tuple], columns: list[str] | tuple) -> Table | None:
    if not data:
        return None

    table = Table()

    for column in columns:
        table.add_column(column)

    for row in data:
        table.add_row(*(str(value) for value in row))

    return table
