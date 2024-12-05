import sys
from pathlib import Path
import streamlit.web.cli as stcli

def main():
    current_dir = Path(__file__).parent
    main_script = current_dir / "main.py"
    sys.argv = ["streamlit", "run", str(main_script)] + sys.argv[1:]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
