from rich.console import Console
from rich.table import Table

from life_analytics.logic import tables


def test_create_table_columns_and_rows():
    table = tables.create_table(
        [("Alice", 10), ("Bob", 20)],
        ["Name", "Score"],
    )
    assert isinstance(table, Table)

    assert [column.header for column in table.columns] == [
        "Name",
        "Score",
    ]
    assert len(table.rows) == 2


def test_create_table_converts_numerical_data_into_strings() -> None:
    table = tables.create_table([(10, 20)], ["Score1", "Score2"])
    assert isinstance(table, Table)

    console = Console()
    console.print(table)  # test if this runs without error
