import typer
from typing import Annotated


def hello(
    arg: Annotated[str, typer.Argument(help="Arg to print")] = "",
    option: Annotated[str, typer.Option(help="Option to print")] = "",
):
    print("Hello from tool-goto-window!")
    print(arg, option)