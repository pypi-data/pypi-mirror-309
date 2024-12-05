import streamlit.web.cli as stcli
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", str(Path(__file__).parent / "learn_genai" / "main.py")] + sys.argv[1:]
    sys.exit(stcli.main())
