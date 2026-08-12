import io
import subprocess
from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta


def format_csv(file: Path | str, format: str) -> str:
    try:
        result = subprocess.run(
            [
                "ledger",
                "--format",
                format,
                "-f",
                str(file),
                "csv",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise e


def read(file: Path | str) -> pd.DataFrame:
    # file = Path("~/wks/ledger/ledger_kakei/journal/kakei/main.ledger")
    # file = Path("~/wks/ledger/ledger_kakei/journal/tadatoshi/cash/wallet.ledger")
    # file = Path("~/wks/ledger/ledger_kakei/journal/kakei/bank/sonybank/sonybank.ledger")

    # format = "%(date),%(payee),%(account),%(quantity(amount)),%(commodity),%(filename),%(beg_line)\n"
    format = "%(date),%(payee),%(account),%(quantity(amount)),%(commodity),%(meta('pay_month')),%(meta('shop')),%(meta('school')),%(meta('label')),%(filename),%(beg_line)\n"
    names = "date payee account amount commodity pay_month shop school label filename lineno".split()

    text = format_csv(file, format)
    stream = io.StringIO(text)
    df = pd.read_csv(
        stream,
        header=None,
        names=names,
        parse_dates=["date"],
        converters={"amount": Decimal},
    )

    return df


def account_list(df: pd.DataFrame) -> list[str]:
    account = df["account"].dropna().drop_duplicates().sort_values().to_list()
    return account


def ledger_balance(df: pd.DataFrame, account: str) -> int:
    today = pd.Timestamp.today().normalize()
    df = df[df["account"] == account]
    df = df[df["date"] <= today]
    return df["amount"].sum()

def filter_accounts(
    df: pd.DataFrame, accounts: list[str], pay_month: date
) -> pd.DataFrame:
    month_str = pay_month.strftime("%Y-%m")
    df = df[df["account"].isin(accounts)]
    df = df[df["pay_month"] == month_str]
    df["total"] = df["amount"].cumsum()
    df = df["date payee account amount total pay_month shop".split()]
    df = df.reset_index(drop=True)

    return df


def total_value(df: pd.DataFrame, pay_month: date) -> Decimal:
    last_month = pay_month - relativedelta(months=1)

    df = df[df["date"].dt.to_period("M") == f"{last_month:%Y-%m}"]

    if len(df) == 0:
        return Decimal("0")

    return Decimal(str(df.iloc[-1]["total"]))
