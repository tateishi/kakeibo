import typer

from kakeibo import commands

app = typer.Typer()

app.add_typer(commands.dump_app)
app.add_typer(commands.web_app)
app.add_typer(commands.count_app)

if __name__ == "__main__":
    app()
