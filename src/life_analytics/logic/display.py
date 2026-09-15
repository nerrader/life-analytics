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


def create_stats_grid(data: dict[str, dict[str, str] | str]) -> Table:
    """Creates a table with no borders and headers,
    to create a dashboard-like display for the stats command
    to use.
    """
    grid = Table.grid(expand=False)

    grid.add_column(width=30, no_wrap=True)
    grid.add_column(no_wrap=True)

    for name, value in data.items():
        if not isinstance(value, dict):
            grid.add_row(name, str(value))
            continue

        grid.add_row("-------------------------", "---------")  # add separator

        grid.add_row(name, "")
        for section_name, section_value in value.items():
            if isinstance(section_value, float):
                section_value = round(section_value, 2)
            grid.add_row(f"\t{section_name}", str(section_value))

    return grid
