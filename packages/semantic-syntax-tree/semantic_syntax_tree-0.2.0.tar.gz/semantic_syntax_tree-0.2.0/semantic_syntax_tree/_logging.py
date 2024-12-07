import logging
from contextvars import ContextVar

from rich.console import Console
from rich.logging import RichHandler

CONSOLE = Console()

FORMAT = "%(message)s"

HANDLER = RichHandler(
    show_time=False,
    rich_tracebacks=True,
    tracebacks_show_locals=True,
    markup=True,
    show_path=False,
    console=CONSOLE,
)

VERBOSE = ContextVar[bool]("VERBOSE", default=False)


def setup_logging(verbose: bool = False) -> None:
    VERBOSE.set(verbose)
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=FORMAT,
        handlers=[HANDLER],
    )
