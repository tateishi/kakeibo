import pandas as pd
import pytest
from kakeibo.services import ledger


@pytest.mark.parametrize(
    "input, expect",[
        (
            pd.DataFrame({
                "account": ["a", "b", "a"],
                "amount": [1, 2, 4],
            }),
            ["a", "b"],
        ),
        (
            pd.DataFrame({
                "account": ["a", "c", "b", "a"],
                "amount": [1, 2, 4, 8],
            }),
            ["a", "b", "c"],
        ),
    ]
)
def test_account(input, expect):
    actual = ledger.account_list(input)
    assert actual == expect
