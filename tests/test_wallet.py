import pandas as pd
import pytest
from kakeibo.services import wallet
from pandas.testing import assert_frame_equal


@pytest.mark.parametrize(
    "input, expect",[
        (
            """
# -*- mode: kinshu; coding: utf-8 -*-
# お母さん財布

#-------------------------------------------------------------
#kinshu    10K  5K  2K  1K 500 100  50  10   5   1         sum
#-------------------------------------------------------------
2022-01-03   0   3   0   7   0   2   1   0   0   1   =   22251
2022-01-05   0   2   0   8   1   4   1   2   1   2   =   18977
            """,
            """
2022-01-03   0   3   0   7   0   2   1   0   0   1   =   22251
2022-01-05   0   2   0   8   1   4   1   2   1   2   =   18977
            """,
        ),
    ]
)
def test_parse_wallet(input, expect):
    actual = wallet.parse_wallet(input)
    assert actual == expect.strip()

@pytest.mark.parametrize(
    "input, expect", [
        (
            """
# -*- mode: kinshu; coding: utf-8 -*-
# お母さん財布

#-------------------------------------------------------------
#kinshu    10K  5K  2K  1K 500 100  50  10   5   1         sum
#-------------------------------------------------------------
2022-01-03   0   3   0   7   0   2   1   0   0   1   =   22251
2022-01-05   0   2   0   8   1   4   1   2   1   2   =   18977
            """,
            pd.DataFrame({
                "date": [pd.Timestamp(2022,1,3), pd.Timestamp(2022,1,5)],
                "y10k": [0, 0],
                "y5k": [3, 2],
                "y2k": [0, 0],
                "y1k": [7, 8],
                "y500": [0, 1],
                "y100": [2, 4],
                "y50": [1, 1],
                "y10": [0, 2],
                "y5": [0, 1],
                "y1": [1, 2],
                "eq": ["=", "="],
                "amount": [22251, 18977],
            }),
        ),
    ])
def test_read_wallet(input, expect):
    actual = wallet.wallet_to_dataframe(input)

    assert_frame_equal(actual, expect)

@pytest.mark.parametrize(
    "input, expect", [
        (
            pd.DataFrame({
                "date": [pd.Timestamp(2022,1,3), pd.Timestamp(2022,1,5)],
                "y10k": [0, 0],
                "y5k": [3, 2],
                "y2k": [0, 0],
                "y1k": [7, 8],
                "y500": [0, 1],
                "y100": [2, 4],
                "y50": [1, 1],
                "y10": [0, 2],
                "y5": [0, 1],
                "y1": [1, 2],
                "eq": ["=", "="],
                "amount": [22251, 18977],
            }),
            18977
        ),
        (
            pd.DataFrame({
                "date": [pd.Timestamp(2022,1,3), pd.Timestamp(2027,1,5)],
                "y10k": [0, 0],
                "y5k": [3, 2],
                "y2k": [0, 0],
                "y1k": [7, 8],
                "y500": [0, 1],
                "y100": [2, 4],
                "y50": [1, 1],
                "y10": [0, 2],
                "y5": [0, 1],
                "y1": [1, 2],
                "eq": ["=", "="],
                "amount": [22251, 18977],
            }),
            22251
        ),
    ])
def test_last_amount(input, expect):
    from datetime import date

    actual = wallet.last_amount(input, date(2026, 8, 6))

    assert actual == expect
