import typer

from .account import count_account_app
from .description import count_desc_app

count_app = typer.Typer()

count_app.add_typer(count_account_app)
count_app.add_typer(count_desc_app)
