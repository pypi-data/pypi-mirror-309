import streamlit.web.cli as stcli
import sys
from pathlib import Path

def main():
    sys.argv = ["streamlit", "run", str(Path(__file__).parent / "main.py")] + sys.argv[1:]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
