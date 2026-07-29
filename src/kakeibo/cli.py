import sys
import subprocess

from .services import ledger


def app():
    try:
        df = ledger.read()
        for row in df.itertuples():
            print(row)
        # print(df)
    except RuntimeError as e:
        print(f"RuntimeError: {e}", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: {e}, {e.stderr}", file=sys.stderr)

if __name__=="__main__":
    app()
