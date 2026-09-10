import subprocess
import sys
from pathlib import Path

from kakeibo import services

import typer

dump_app = typer.Typer()

@dump_app.command()
def dump():
    try:
        file = Path("~/wks/ledger/ledger_kakei/journal/kakei/main.ledger")
        df = services.read_ledger(file)
        for row in df.itertuples():
            print(row)
    except RuntimeError as e:
        print(f"RuntimeError: {e}", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: {e}, {e.stderr}", file=sys.stderr)
