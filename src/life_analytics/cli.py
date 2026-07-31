from typing import Annotated

import questionary
import typer

from life_analytics import constants as const
from life_analytics import database

app = typer.Typer()


@app.command("summary")
def add_daily_summary() -> None:
    pass


@app.command("activity")
def add_activity() -> None:
    pass


@app.command("sleep")
def add_sleep() -> None:
    pass


@app.command("stats")
def show_stats() -> None:
    pass


@app.command("clear")
def clear_all_data(
    skip_confirm: Annotated[
        bool | None, typer.Option("--skip", "-s", help="Skips the confirmation prompt.")
    ] = None,
) -> None:

    clear_data_confirm = questionary.confirm(
        "Are you sure you want to clear all data from the database?"
    ).skip_if(skip_confirm == True, default=True)

    if clear_data_confirm:
        database.clear_database(const.LIFE_DATABASE_FILEPATH)
