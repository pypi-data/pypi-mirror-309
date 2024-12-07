import logging
from pathlib import Path
from typing import Annotated

import typer

from semantic_syntax_tree._git import git_repo_name
from semantic_syntax_tree._logging import CONSOLE
from semantic_syntax_tree.context import (
    CHROMA_CLIENT,
    CHROMA_EMBEDDING_FUNCTION,
)
from semantic_syntax_tree.database import get_search_results
from semantic_syntax_tree.models import SstSearchResult

LOG = logging.getLogger(__name__)


def search(
    query: Annotated[
        str, typer.Argument(help="The text which we will use for semantic search")
    ],
    *,
    n: Annotated[int, typer.Option("-n", help="The max number of results")] = 10,
    repo: Annotated[
        Path | None,
        typer.Option(
            "--repo",
            "-r",
            help="The filepath of the source repository, defaults to the current directory",
        ),
    ] = None,
    collection_name: Annotated[
        str | None,
        typer.Option(
            "--collection-name",
            "-c",
            help="The name of the collection in the vector database. Defaults to the repository name.",
        ),
    ] = None,
) -> list[SstSearchResult]:
    """
    Search the vector database for semantic similarity to the given query.
    """
    repo = (repo or Path(".")).resolve()
    collection_name = collection_name or git_repo_name(repo)

    client = CHROMA_CLIENT.get()
    embedding_function = CHROMA_EMBEDDING_FUNCTION.get()
    assert embedding_function is not None, "No embedding function found"

    CONSOLE.print(f"Searching for snippets similar to '[magenta]{query}[/magenta]'")

    collection = client.get_or_create_collection(
        collection_name,
        embedding_function=embedding_function,
    )
    results = get_search_results(collection, query, n)

    CONSOLE.print(*results, sep="\n\n")

    return results
