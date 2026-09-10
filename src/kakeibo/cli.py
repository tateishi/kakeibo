import typer

from kakeibo import commands

app = typer.Typer()

app.add_typer(commands.app)

if __name__ == "__main__":
    app()
