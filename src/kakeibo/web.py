import subprocess
import sys
from pathlib import Path

def app():
    webapp = Path(__file__).parent / "webapp/app.py"

    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(webapp),
    ])

if __name__ == "__main__":
    app()
