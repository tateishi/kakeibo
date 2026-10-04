import typer

from kakeibo.commands import count_commands

count_app = typer.Typer()

count_app.add_typer(count_commands.count_account_app)
count_app.add_typer(count_commands.count_desc_app)
