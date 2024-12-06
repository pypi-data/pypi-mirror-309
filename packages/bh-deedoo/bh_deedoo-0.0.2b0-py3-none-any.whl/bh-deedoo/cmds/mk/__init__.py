#!/usr/bin/env python
import subprocess
import os
from pathlib import Path

import typer

from .templates import BASH, PYTHON

EDITOR=os.environ.get("EDITOR")

app=typer.Typer()

@app.command()
def sh(name: str):
    file=Path(name)
    if file.exists():
        print( f'File {name} already esists.' )
        exit(1)
    file.write_text( BASH.strip() % (name,name) )
    file.chmod( 0o755 )
    if EDITOR:
        subprocess.run( [ EDITOR, str(file) ] )


@app.command()
def py(name: str):
    file=Path(name)
    if file.exists():
        print( f'File {name} already esists.' )
        exit(1)
    file.write_text( PYTHON.strip() )
    file.chmod( 0o755 )
    if EDITOR:
        subprocess.run( [ EDITOR, str(file) ] )

