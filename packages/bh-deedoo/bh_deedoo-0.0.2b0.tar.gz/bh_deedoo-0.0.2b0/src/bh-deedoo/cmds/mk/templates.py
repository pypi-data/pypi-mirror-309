#!/usr/bin/env python

BASH = """\
#!/usr/bin/env bash
[ $0. == ./%s. ] || { echo try ./%s ; exit 1; }
echo ++[$0] ["$@"]
echo --[$0]
"""

PYTHON = """\
#!/usr/bin/env python3
import os
import sys
from pathlib import Path
THIS=Path(__file__)

def main():
    print(THIS)
    print(sys.argv)

if __name__ == "__main__":
    main()
"""
