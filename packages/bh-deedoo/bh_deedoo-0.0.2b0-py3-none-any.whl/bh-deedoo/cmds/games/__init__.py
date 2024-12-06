import typer
from . import pool

app = typer.Typer()

@app.command()
def chess():
    pass

@app.command()
def checkers():
    pass

app.add_typer(pool.app, name="que-games")
