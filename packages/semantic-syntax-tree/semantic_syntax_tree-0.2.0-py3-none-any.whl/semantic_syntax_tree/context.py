"""
Globals and thread-local context variables that are used throughout the package.

TODO: maybe make stuff that depends on expensive imports lazy-loaded?
"""

import os
import platform
from contextvars import ContextVar
from typing import Optional, cast

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.types import (
    Embeddable,
    EmbeddingFunction,
)
from chromadb.utils import embedding_functions


def default_chroma_client() -> ClientAPI:
    """Return the default ClientAPI for the current system."""
    host = CHROMA_DATABASE_HOST.get()
    if host:
        return chromadb.HttpClient(host=host, port=CHROMA_DATABASE_PORT.get())
    return chromadb.PersistentClient(path=CHROMA_DATABASE_DIRECTORY.get())


def default_chroma_embedding_function() -> Optional[EmbeddingFunction[Embeddable]]:
    """
    Return the default EmbeddingFunction for the current system.
    This accounts for an issue with the default EmbeddingFunction on Intel-based Macs from ~2019-2020:
    https://github.com/chroma-core/chroma/issues/2731
    """
    system = platform.system()
    machine = platform.machine()

    # Check if it's a Mac
    is_mac = system == "Darwin"
    # Check if it's Intel (x86_64) rather than ARM (arm64)
    is_intel = machine in ("x86_64", "AMD64", "i386")

    if is_mac and is_intel:
        from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import (
            ONNXMiniLM_L6_V2,
        )

        return cast(
            EmbeddingFunction[Embeddable],
            ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"]),
        )

    return cast(
        Optional[EmbeddingFunction[Embeddable]],
        embedding_functions.DefaultEmbeddingFunction(),
    )


CHROMA_DATABASE_DIRECTORY = ContextVar[str](
    "CHROMA_DATABASE_DIRECTORY",
    default=os.getenv("CHROMA_DATABASE_DIRECTORY", "./chroma"),
)

CHROMA_DATABASE_HOST = ContextVar[str | None](
    "CHROMA_DATABASE_HOST",
    default=os.getenv("CHROMA_DATABASE_HOST") or None,
)

CHROMA_DATABASE_PORT = ContextVar[int](
    "CHROMA_DATABASE_PORT",
    default=int(os.getenv("CHROMA_DATABASE_PORT", "8000")),
)

CHROMA_CLIENT: ContextVar[ClientAPI] = ContextVar(
    "CHROMA_CLIENT",
    default=default_chroma_client(),
)

CHROMA_EMBEDDING_FUNCTION: ContextVar[EmbeddingFunction[Embeddable] | None] = (
    ContextVar(
        "CHROMA_EMBEDDING_FUNCTION",
        default=default_chroma_embedding_function(),
    )
)
