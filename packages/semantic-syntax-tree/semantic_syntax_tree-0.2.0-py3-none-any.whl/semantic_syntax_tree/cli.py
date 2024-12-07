import typer

from semantic_syntax_tree._logging import setup_logging
from semantic_syntax_tree.search import search
from semantic_syntax_tree.sync import sync

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)
app.command("search", no_args_is_help=True)(search)
app.command("sync")(sync)


@app.callback(invoke_without_command=True)
def callback(verbose: bool = False):
    """
    [bold]Semantic Syntax Tree CLI[/bold]

    Explore python code as an AST indexed by a vector database.
    Learn more: [link]https://github.com/phillipdupuis/semantic-syntax-tree[/link]
    """
    setup_logging(verbose=verbose)
