import typer

app = typer.Typer()


@app.command("summary")
def add_daily_summary():
    pass


@app.command("activity")
def add_activity():
    pass


@app.command("sleep")
def add_sleep():
    pass


@app.command("stats")
def show_stats():
    pass


@app.command("clear")
def clear_all_data():
    pass
