import io
from datetime import date
from pathlib import Path

import pandas as pd


def parse_wallet(text: str) -> str:
    text = [
        line for line in text.splitlines() if len(line) > 0 and line[0] in "0123456789"
    ]
    return "\n".join(text)


def wallet_to_dataframe(text: str) -> pd.DataFrame:
    text = parse_wallet(text)

    names = "date y10k y5k y2k y1k y500 y100 y50 y10 y5 y1 eq amount".split()

    df = pd.read_csv(
        io.StringIO(text), header=None, names=names, parse_dates=["date"], sep=r"\s+"
    )

    return df


def read_wallet(path: Path | str) -> pd.DataFrame:
    text = path.read_text()
    return wallet_to_dataframe(text)


def last_amount(df: pd.DataFrame, date: date | None = None) -> int:
    if date is None:
        date = pd.Timestamp.today().normalize()
    else:
        date = pd.Timestamp(date).normalize()

    df_past = df[df["date"] <= date]
    nearest = df_past.loc[(date - df_past["date"]).abs().idxmin()]

    return nearest["amount"]
