import typer
from pathlib import Path
import datetime
import sys
import string
import os
from typing import List
ZJOT_ACC=os.environ.get("ZJOT_ACC") or Path.home()/"ZJOT"
ZJOT_ACC=Path(ZJOT_ACC)
ZJOT_ACC.is_dir() or ZJOT_ACC.mkdir()

app = typer.Typer()

@app.command()
def show ( acc: str=ZJOT_ACC ):
    STORE=Path(acc)
    for file in sorted(STORE.glob('*.zjot.acc')):
        print( f"""---------------------- {file.name}""")
        print( file.read_text() )
    print( f"""---------------------- {ZJOT_ACC}""")
    for file in sorted(STORE.glob('*.zjot')):
        line = file.read_text().strip()
        print( line )

@app.command()
def new (args: List[str] ):
    now = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    left = (' '.join(args)).strip()

    show()
    print (f">>>>>>>>>>>>>>>>>>>>>> {left} |" )
    right = input().strip()

    if not (left or right):
        exit( 'no jot entered' )
    if False in [ ch in string.printable for ch in left + right ]:
        exit( 'cannot jot line with unprintable characters:' )

    line=f"{now} [zjot] {left} | {right}"
    (ZJOT_ACC/f"{now}.zjot").write_text(line)
    show()

@app.command()
def join ():
    def text4zjot(zjot):
        assert zjot.name.endswith('.zjot')
        return zjot.read_text().strip()+'\n'
    files = list(sorted(ZJOT_ACC.glob('*.zjot')))
    lines = list(map(text4zjot, files))
    block = ''.join(lines)
    first = files[0]
    join_file = Path(f"{first}.acc")
    join_file.write_text(block)
    for file in files:
        os.remove(file)


if __name__=='__main__':
    main()
