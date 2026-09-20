import subprocess
import sys
from importlib.resources import files

import typer

web_app = typer.Typer()


@web_app.command()
def web():
    webapp = files("kakeibo.webapp").joinpath("app.py")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(webapp),
        ]
    )
