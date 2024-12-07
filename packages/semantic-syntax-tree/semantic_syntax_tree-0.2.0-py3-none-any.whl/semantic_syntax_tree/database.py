import logging
from typing import Iterable, cast

from chromadb.api.models.Collection import Collection  # type: ignore
from chromadb.api.types import (
    Document,
    Documents,
    EmbeddingFunction,
    Metadata,
)

from semantic_syntax_tree.models import (
    QualifiedName,
    SstNode,
    SstNodeMetadata,
    SstSearchResult,
)

LOG = logging.getLogger(__name__)


def add_nodes(
    collection: Collection,
    embedding_function: EmbeddingFunction[Documents],
    nodes: list[SstNode],
) -> None:
    """Add SstNodes to the collection."""
    if not nodes:
        return
    LOG.info(f"Adding {len(nodes)} nodes to '{collection.name}'")
    collection.add(
        ids=[node.id for node in nodes],
        documents=[node.document for node in nodes],
        embeddings=embedding_function(input=[node.code for node in nodes]),
        metadatas=[cast(Metadata, node.metadata) for node in nodes],
    )


def update_nodes(
    collection: Collection,
    embedding_function: EmbeddingFunction[Documents],
    nodes: list[SstNode],
) -> None:
    """Update SstNodes in the collection."""
    if not nodes:
        return
    LOG.info(f"Updating {len(nodes)} nodes in '{collection.name}'")
    embeddings = embedding_function(input=[node.code for node in nodes])
    collection.update(
        ids=[node.id for node in nodes],
        documents=[node.document for node in nodes],
        embeddings=embeddings,
        metadatas=[cast(Metadata, node.metadata) for node in nodes],
    )


def update_metadatas(
    collection: Collection,
    nodes: list[SstNode],
) -> None:
    """Update the metadata for SstNodes in the collection."""
    if not nodes:
        return
    LOG.info(f"Updating metadata for {len(nodes)} nodes in '{collection.name}'")
    collection.update(
        ids=[node.id for node in nodes],
        metadatas=[cast(Metadata, node.metadata) for node in nodes],
    )


def delete_nodes(collection: Collection, ids: Iterable[str]) -> None:
    """Delete SstNodes from the collection."""
    ids = list(ids)
    LOG.info(f"Deleting {len(ids)} nodes from '{collection.name}'")
    collection.delete(ids=ids)


def get_ids(collection: Collection, file: str | None = None) -> list[QualifiedName]:
    """Return the unique ids in the collection."""
    result = collection.get(where={"file": file}) if file else collection.get()
    return [id for id in result["ids"]]


def get_metadatas(
    collection: Collection,
    file: str | None = None,
) -> dict[QualifiedName, SstNodeMetadata]:
    """Return the matching metadatas in the collection."""
    result = collection.get(where={"file": file}) if file else collection.get()
    ids = result["ids"]
    metadatas = cast(list[SstNodeMetadata], result["metadatas"])
    return {id: metadata for id, metadata in zip(ids, metadatas)}


def get_nodes(
    collection: Collection,
    file: str | None = None,
) -> dict[QualifiedName, SstNode]:
    """Return the matching SstNode instances in the collection."""
    result = collection.get(where={"file": file}) if file else collection.get()
    ids = result["ids"]
    documents = cast(list[Document], result["documents"])
    metadatas = cast(list[Metadata], result["metadatas"])
    return {
        id: SstNode.from_db_values(id=id, document=document, metadata=metadata)
        for (id, document, metadata) in zip(ids, documents, metadatas)
    }


def get_search_results(
    collection: Collection,
    query: str,
    n: int = 10,
) -> list[SstSearchResult]:
    """Return the top n search results for a query based on semantic similarity."""
    result = collection.query(query_texts=[query], n_results=n)
    # The results are all nested lists which correspond positionally to items in the query_texts list
    assert len(result["ids"]) == 1, "Expected a single query result"
    ids = result["ids"][0]
    documents = cast(list[list[Document]], result["documents"])[0]
    metadatas = cast(list[list[Metadata]], result["metadatas"])[0]
    distances = cast(list[list[float]], result["distances"])[0]
    return [
        SstSearchResult(
            node=SstNode.from_db_values(id=id, document=document, metadata=metadata),
            query=query,
            distance=distance,
        )
        for id, document, metadata, distance in zip(
            ids, documents, metadatas, distances
        )
    ]
