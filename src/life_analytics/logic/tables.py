from collections.abc import Sequence
from typing import Any, Final

from rich.table import Table

SUMMARY_COLUMNS: Final[tuple[str, ...]] = (
    "Summary Date",
    "Mood",
    "Productivity",
    "Stress",
)
ACTIVITY_COLUMNS: Final[tuple[str, ...]] = (
    "Activity ID",
    "Acitivity Date",
    "Activity Category",
    "Acitivity Description",
    "Activity Start",
    "Activity End",
    "Effort",
    "Enjoyability",
)
SLEEP_COLUMNS: Final[tuple[str, ...]] = (
    "Sleep ID",
    "Sleep Start Time",
    "Sleep End Time",
    "Sleep Quality",
    "Sleep Type",
)


def to_db_column_name(column_name: str) -> str:
    """Converts the capitalized, preferred names to the column names used by the databases.

    Args:
        column_name: The regular column name to convert.

    Returns:
        (str): The database column equivalent.
    """
    return column_name.lower().replace(" ", "_")


def create_table(
    data: Sequence[Any], columns: list[str] | tuple[str, ...]
) -> Table | None:
    if not data:
        return None

    table = Table()

    for column in columns:
        table.add_column(column)

    for row in data:
        table.add_row(*(str(value) for value in row))

    return table
