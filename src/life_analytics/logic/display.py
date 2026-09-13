from collections.abc import Sequence
from typing import Any

from rich.table import Table


# its not the best way, but its better than making a constant dictionary mapping
def db_to_table_column_name(column_name: str) -> str:
    return column_name.strip().replace("_", " ").title()


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


def create_stats_grid() -> Table:
    """Creates a table with no borders and headers,
    to create a dashboard-like display for the stats command
    to use.
    """
    grid = Table.grid()

    grid.add_column()
    grid.add_column()

    return grid


def create_grid_section(grid: Table, title: str, contents: dict[str, str]) -> None:
    grid.add_row(title, "")
    for name, value in contents.items():
        grid.add_row("\tname", "value")
