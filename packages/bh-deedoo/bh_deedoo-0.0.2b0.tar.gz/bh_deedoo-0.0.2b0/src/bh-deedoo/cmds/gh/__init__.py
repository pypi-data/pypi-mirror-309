import typer

app = typer.Typer()


from subprocess import run
from pprint import pprint
import sys
from pathlib import Path
import subprocess
import typer
import os

SCRIPT = str( Path(__file__).parent/'delete-tmp-repo.expect' )


def repos():
    it=run('my gh repos list'.split(), text=True, capture_output=True )
    repos = it.stdout.split('\n')
    repos = [ x for x in repos if len(x.split()) == 1 ]
    return repos

@app.command()
def demo():
    """Demonstrate [clean]
    """
    run( 'gh repo create tmp-foo --public'.split() )
    run( 'gh repo create tmp-bar --private'.split() )
    clean()
@app.command()
def clean():
    """Delete [tmp-*] repos from github
    """
    names = [ x[4:] for x in repos() if x.startswith('tmp-') ]
    for name in names:
        run( [SCRIPT, name] )

if __name__ == '__main__':
    app()
