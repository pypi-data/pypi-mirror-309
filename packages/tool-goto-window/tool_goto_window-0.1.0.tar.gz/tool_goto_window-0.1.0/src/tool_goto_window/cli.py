import typer

from tool_goto_window.main import hello


app = typer.Typer()
app.command()(hello)


if __name__ == "__main__":
    app()