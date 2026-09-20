import pytest

from kakeibo.services import ledger

SCHEME = [
    ("date", "%(date)"),
    ("payee", "%(payee)"),
    ("account", "%(account)"),
    ("amount", "%(quantity(amount))"),
    ("commodity", "%(commodity)"),
    ("pay_month", "%(meta('pay_month'))"),
    ("shop", "%(meta('shop'))"),
    ("school", "%(meta('school'))"),
    ("label", "%(meta('label'))"),
    ("filename", "%(filename)"),
    ("lineno", "%(beg_line)"),
]


@pytest.mark.parametrize(
    "input, expect",
    [
        (
            SCHEME,
            (
                "%(date),"
                "%(payee),"
                "%(account),"
                "%(quantity(amount)),"
                "%(commodity),"
                "%(meta('pay_month')),"
                "%(meta('shop')),"
                "%(meta('school')),"
                "%(meta('label')),"
                "%(filename),"
                "%(beg_line)"
                "\n"
            ),
        )
    ],
)
def test_scheme_format(input: list[tuple[str, str]], expect: str):
    actual = ledger.build_format(input)
    assert actual == expect


@pytest.mark.parametrize(
    "input, expect",
    [
        (
            SCHEME,
            [
                "date",
                "payee",
                "account",
                "amount",
                "commodity",
                "pay_month",
                "shop",
                "school",
                "label",
                "filename",
                "lineno",
            ],
        )
    ],
)
def test_scheme_names(input: list[tuple[str, str]], expect: list[str]):
    actual = ledger.build_names(input)
    assert actual == expect
