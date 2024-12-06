import subprocess
from pathlib import Path

import typer

from bh import STORE
app = typer.Typer()

@app.command()
def gist():
    gstore = STORE/'gists'
    gists = list(gstore.glob('*'))
    for ii, gist in enumerate(gists):
        print(ii, gist.name)
    ii = input('enter number: ')
    try:
        gist = gists[ int(ii) ]
    except (ValueError, IndexError):
        return
    subprocess.run( f'vi {str(gist)}'.split() )
@app.command()
def null():
    pass

