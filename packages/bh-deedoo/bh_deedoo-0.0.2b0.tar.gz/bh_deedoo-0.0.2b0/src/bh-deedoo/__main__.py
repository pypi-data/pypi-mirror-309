import typer
import sys
import subprocess
from pathlib import Path
from .cmds import fruit
from .cmds import games
from .cmds import mk
from .cmds import gh
from .cmds import notes
from .cmds import zjot

app = typer.Typer()
app.add_typer(zjot.app, name="zjot")
app.add_typer(fruit.app, name="fruit")
app.add_typer(games.app, name="games")
app.add_typer(mk.app, name="mk")
app.add_typer(gh.app, name="gh")
app.add_typer(notes.app, name="notes")

@app.command()
def profile():
    env=Path(__file__).parent.parent.parent/'env'
    print(f"export BH_BH_ENV={env}; source {env}/profile")

@app.command()
def bashrc():
    env=Path(__file__).parent.parent.parent/'env'
    bin=Path(__file__).parent.parent.parent/'bin'
    print( f"""
    export BH_BH_ENV={env};
    export BH_BH_BIN={bin};
    source {env}/bashrc
    """)

@app.command()
def install():
    real=Path(__file__).parent.parent.parent/'.venv/bin/bh'
    link=Path.home()/'.local/bin/bh'
    try:
        link.unlink()
    except FileNotFoundError:
        pass
    link.symlink_to(real)
    print( 'done' )

@app.command()
def main():
    app()


