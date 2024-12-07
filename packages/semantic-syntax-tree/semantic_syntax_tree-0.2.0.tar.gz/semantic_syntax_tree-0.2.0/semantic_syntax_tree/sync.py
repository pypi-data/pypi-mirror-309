import logging
from fnmatch import fnmatch
from pathlib import Path
from typing import Annotated, NamedTuple

import typer
from rich.progress import track
from rich.rule import Rule

from semantic_syntax_tree._git import git_list_files, git_repo_name
from semantic_syntax_tree._logging import CONSOLE, VERBOSE
from semantic_syntax_tree.context import (
    CHROMA_CLIENT,
    CHROMA_EMBEDDING_FUNCTION,
)
from semantic_syntax_tree.database import (
    add_nodes,
    delete_nodes,
    get_metadatas,
    update_metadatas,
    update_nodes,
)
from semantic_syntax_tree.models import QualifiedName, SstNode, SstNodeMetadata
from semantic_syntax_tree.parsers import parse_python_module

LOG = logging.getLogger(__name__)


def sync(
    repo: Annotated[
        Path | None,
        typer.Argument(
            help="The path of the source repository, defaults to the current directory",
        ),
    ] = None,
    collection_name: Annotated[
        str | None,
        typer.Option(
            "--collection-name",
            "-c",
            help="The name of the collection in the vector database to sync with. Defaults to the repository name.",
        ),
    ] = None,
    include: Annotated[
        list[str] | None,
        typer.Option(
            "-i",
            "--include",
            help="Include files only if the match the given glob patterns.",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "-e", "--exclude", help="Exclude files that match these patterns."
        ),
    ] = None,
    delete: Annotated[
        bool,
        typer.Option(
            "--delete",
            help="Clean up the database by deleting any nodes which match the include/exclude patterns but do not exist in the repository",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Print the commands that would be run without actually executing them",
        ),
    ] = False,
) -> None:
    """
    Sync the python code in a git repository with a vector database.
    """
    repo = (repo or Path(".")).resolve()
    collection_name = collection_name or git_repo_name(repo)
    include = include or []
    exclude = exclude or []

    client = CHROMA_CLIENT.get()
    embedding_function = CHROMA_EMBEDDING_FUNCTION.get()
    assert embedding_function is not None, "No embedding function found"

    CONSOLE.print(
        f"Syncing [green]{repo}[/green] with collection [yellow]{collection_name}[/yellow]"
    )

    collection = client.get_or_create_collection(
        collection_name, embedding_function=embedding_function
    )

    nodes_in_db = get_metadatas(collection)
    files_in_db = {metadata["file"] for metadata in nodes_in_db.values()}

    CONSOLE.print(
        f"[yellow]{len(nodes_in_db)}[/yellow] nodes currently exist in [yellow]{collection_name}[/yellow]"
    )
    CONSOLE.print(
        f"[yellow]{len(files_in_db)}[/yellow] files currently exist in [yellow]{collection_name}[/yellow]"
    )

    nodes_generated: list[SstNode] = []
    files = _get_python_files(repo, include, exclude)

    CONSOLE.print(
        f"[blue]{len(files)}[/blue] python files from [blue]{repo}[/blue] will be synced"
    )

    for path in track(files, console=CONSOLE, description="Parsing python files"):
        CONSOLE.print(Rule(f"{path.relative_to(repo)}", style="green"))

        nodes = parse_python_module(path, repo)
        nodes_generated += nodes
        CONSOLE.print(f"{len(nodes)} nodes found in [green]{path}[/green]")

        status = _group_by_status(nodes, nodes_in_db)

        _describe_nodes(
            status.synced, f"are synced with [yellow]{collection_name}[/yellow]"
        )

        if dry_run:
            _describe_nodes(status.new, "will be created")
            _describe_nodes(status.updated_document, "will be re-embedded and updated")
            _describe_nodes(status.updated_metadata, "will have metadata-only updates")
        else:
            add_nodes(collection, embedding_function, status.new)
            update_nodes(collection, embedding_function, status.updated_document)
            update_metadatas(collection, status.updated_metadata)

    if delete:
        ids = _get_ids_to_delete(nodes_generated, nodes_in_db, repo, include, exclude)
        if ids:
            CONSOLE.print(Rule("Deleting nodes", style="red"))
            if dry_run:
                _describe_nodes(list(ids), "nodes will be deleted")
            else:
                delete_nodes(collection, ids)


def _get_python_files(repo: Path, include: list[str], exclude: list[str]) -> list[Path]:
    """
    Get all python files in a git repository that satisfy the include and exclude patterns.?
    """
    return [
        path
        for path in git_list_files(repo)
        if _is_valid_path(path, repo, include, exclude)
    ]


def _is_valid_path(
    path: Path, repo: Path, include: list[str], exclude: list[str]
) -> bool:
    """
    Check if the path is for a .py file that satisfies the include and exclude patterns.
    """
    if path.suffix != ".py":
        return False
    name = str(path.relative_to(repo) if path.is_absolute() else path)
    if include and not any(fnmatch(name, pattern) for pattern in include):
        return False
    if exclude and any(fnmatch(name, pattern) for pattern in exclude):
        return False
    return True


class _StatusGroups(NamedTuple):
    new: list[SstNode]
    synced: list[SstNode]
    updated_document: list[SstNode]
    updated_metadata: list[SstNode]


def _group_by_status(
    nodes: list[SstNode], nodes_in_db: dict[QualifiedName, SstNodeMetadata]
) -> _StatusGroups:
    """
    Group nodes by their change status relative to the nodes in the database.
    """
    new: list[SstNode] = []
    synced: list[SstNode] = []
    updated_document: list[SstNode] = []
    updated_metadata: list[SstNode] = []

    for node in nodes:
        db_metadata = nodes_in_db.get(node.id)
        if db_metadata is None:
            new.append(node)
        elif db_metadata == node.metadata:
            synced.append(node)
        elif db_metadata["sha1_hash"] != node.metadata["sha1_hash"]:
            updated_document.append(node)
        else:
            updated_metadata.append(node)

    return _StatusGroups(new, synced, updated_document, updated_metadata)


def _describe_nodes(nodes: list[SstNode] | list[str], description: str) -> None:
    """Print a status for a group of nodes."""
    if not nodes:
        return
    CONSOLE.print(f"{len(nodes)} {description}")
    if VERBOSE.get():
        for node in nodes:
            CONSOLE.print(f" - {node.id if isinstance(node, SstNode) else node}")


def _get_ids_to_delete(
    nodes_generated: list[SstNode],
    nodes_in_db: dict[QualifiedName, SstNodeMetadata],
    repo: Path,
    include: list[str],
    exclude: list[str],
) -> set[str]:
    """
    Return the ids for nodes that should be deleted from the vector database.
    This only applies to nodes that satisfy the filepath filters BUT
    which are not present in the generated nodes.
    """
    ids_generated = {node.id for node in nodes_generated}
    return {
        id
        for id in nodes_in_db
        if id not in ids_generated
        and _is_valid_path(Path(nodes_in_db[id]["file"]), repo, include, exclude)
    }
