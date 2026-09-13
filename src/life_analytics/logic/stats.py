from rich.table import Table


def create_stats_grid() -> Table:
    """Creates a table with no borders and headers,
    to create a dashboard-like display for the stats command
    to use.
    """
    grid = Table.grid()

    grid.add_column()
    grid.add_column()

    return grid
