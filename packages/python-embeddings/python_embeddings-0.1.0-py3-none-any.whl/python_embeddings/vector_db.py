import logging
import os
import platform
from typing import Iterable, Optional, TypeAlias, cast

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection  # type: ignore
from chromadb.api.types import (
    Document,
    Documents,
    EmbeddingFunction,
    Metadata,
)
from chromadb.utils import embedding_functions

from python_embeddings.code_parsers import (
    PythonNode,
    PythonNodeMetadata,
    QualifiedName,
)

PythonNodeIds: TypeAlias = list[QualifiedName]
PythonNodeMetadatas: TypeAlias = dict[QualifiedName, PythonNodeMetadata]
PythonNodes: TypeAlias = dict[QualifiedName, PythonNode]


LOG = logging.getLogger(__name__)
CHROMADB_DATA_DIR = os.getenv("CHROMADB_DATA_DIR", "./chroma")


def default_client() -> ClientAPI:
    """Return the default ClientAPI for the current system."""
    return chromadb.PersistentClient(path=CHROMADB_DATA_DIR)


def default_embedding_function() -> Optional[EmbeddingFunction[Documents]]:
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
            EmbeddingFunction[Documents],
            ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"]),
        )

    return embedding_functions.DefaultEmbeddingFunction()


def add_nodes(
    collection: Collection,
    embedding_function: EmbeddingFunction[Documents],
    nodes: list[PythonNode],
) -> None:
    """Add PythonNodes to the collection."""
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
    nodes: list[PythonNode],
) -> None:
    """Update PythonNodes in the collection."""
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
    nodes: list[PythonNode],
) -> None:
    """Update the metadata for PythonNodes in the collection."""
    if not nodes:
        return
    LOG.info(f"Updating metadata for {len(nodes)} nodes in '{collection.name}'")
    collection.update(
        ids=[node.id for node in nodes],
        metadatas=[cast(Metadata, node.metadata) for node in nodes],
    )


def delete_nodes(collection: Collection, ids: Iterable[str]) -> None:
    """Delete PythonNodes from the collection."""
    ids = list(ids)
    LOG.info(f"Deleting {len(ids)} nodes from '{collection.name}'")
    collection.delete(ids=ids)


def get_ids(collection: Collection, file: str | None = None) -> PythonNodeIds:
    """Return the unique ids in the collection."""
    result = collection.get(where={"file": file}) if file else collection.get()
    return [id for id in result["ids"]]


def get_metadatas(
    collection: Collection,
    file: str | None = None,
) -> dict[QualifiedName, PythonNodeMetadata]:
    """Return the matching metadatas in the collection."""
    result = collection.get(where={"file": file}) if file else collection.get()
    ids = result["ids"]
    metadatas = cast(list[PythonNodeMetadata], result["metadatas"])
    return {id: metadata for id, metadata in zip(ids, metadatas)}


def get_nodes(
    collection: Collection,
    file: str | None = None,
) -> dict[QualifiedName, PythonNode]:
    """Return the matching PythonNode instances in the collection."""
    result = collection.get(where={"file": file}) if file else collection.get()
    ids = result["ids"]
    documents = cast(list[Document], result["documents"])
    metadatas = cast(list[Metadata], result["metadatas"])
    return {
        id: PythonNode.from_db_values(id=id, document=document, metadata=metadata)
        for (id, document, metadata) in zip(ids, documents, metadatas)
    }
