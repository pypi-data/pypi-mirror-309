import argparse
import logging
from fnmatch import fnmatch
from pathlib import Path
from typing import Literal, NamedTuple, Sequence

from tqdm import tqdm

from python_embeddings.code_parsers import (
    PythonNode,
    parse_python_module,
)
from python_embeddings.git_utils import git_list_files, git_repo_name

from python_embeddings.log_utils import log_message_prefix
from python_embeddings.vector_db import (
    ClientAPI,
    PythonNodeMetadatas,
    add_nodes,
    default_client,
    default_embedding_function,
    delete_nodes,
    get_metadatas,
    update_metadatas,
    update_nodes,
)

LOG = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> Literal[0, 1]:
    """
    Command-line interface for syncing the python code in a git repository with a vector database.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "repo",
        type=str,
        nargs="?",
        default=".",
        help="The filepath of the source repository, defaults to the current directory",
    )
    parser.add_argument(
        "-c",
        "--collection",
        type=str,
        nargs="?",
        default=None,
        help="The name of the collection in the vector database to sync with. Defaults to the repository name.",
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        nargs="+",
        help="Include files only if the match the given glob patterns. "
        "If this argument is omitted, all .py files are included by default.",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        nargs="+",
        help="Exclude files that match the given glob patterns.",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete nodes that are in the database but not in the repository",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the commands that would be run without executing them",
    )
    parser.add_argument("--verbose", action="store_true", help="Print debug-level logs")

    try:
        args = parser.parse_args(argv)
        repo = Path(args.repo).resolve()
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.INFO,
            format="%(asctime)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        sync(
            repo=repo,
            client=default_client(),
            collection_name=args.collection or git_repo_name(repo),
            include=args.include or [],
            exclude=args.exclude or [],
            delete=args.delete,
            dry_run=args.dry_run,
        )
        LOG.info("Sync complete")
        return 0

    except Exception:
        LOG.exception("An error occurred")
        return 1


def sync(
    repo: Path,
    client: ClientAPI,
    collection_name: str,
    include: list[str],
    exclude: list[str],
    delete: bool,
    dry_run: bool,
) -> None:
    """
    Sync the python code in a git repository with a vector database.
    """
    embedding_function = default_embedding_function()
    assert embedding_function is not None, "No embedding function found"

    collection = client.get_or_create_collection(collection_name)

    nodes_seen: list[PythonNode] = []

    nodes_in_db = get_metadatas(collection)
    files_in_db = {metadata["file"] for metadata in nodes_in_db.values()}
    LOG.info(f"{len(files_in_db)} files currently exist in '{collection_name}'")
    LOG.info(f"{len(nodes_in_db)} nodes currently exist in '{collection_name}'")

    files = _get_python_files(repo, include, exclude)
    LOG.info(f"{len(files)} python files will be parsed")

    for path in tqdm(files, desc="Parsing files"):
        LOG.info(f"{path.relative_to(repo)}")

        with log_message_prefix("\t"):
            nodes = parse_python_module(path, repo)
            LOG.info(f"Extracted {len(nodes)} nodes")

            nodes_seen.extend(nodes)

            status = _group_by_status(nodes, nodes_in_db)

            if dry_run:
                _describe_nodes(status.synced, "are synced")
                _describe_nodes(status.new, "will be created")
                _describe_nodes(status.updated_document, "will be updated")
                _describe_nodes(
                    status.updated_metadata, "will have their metadata updated"
                )
            else:
                _describe_nodes(status.synced, "are synced")
                add_nodes(collection, embedding_function, status.new)
                update_nodes(collection, embedding_function, status.updated_document)
                update_metadatas(collection, status.updated_metadata)

    if delete:
        ids = _get_ids_to_delete(nodes_seen, nodes_in_db, repo, include, exclude)
        if ids:
            if dry_run:
                _describe_nodes(list(ids), "will be deleted")
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


def _relative_filename(path: Path, repo: Path) -> str:
    """
    Get the 'id' for this file in the context of the repository.
    This allows the values stored in db to be agnostic of the absolute path.
    """
    return str(path.relative_to(repo) if path.is_absolute() else path)


def _is_valid_path(
    path: Path, repo: Path, include: list[str], exclude: list[str]
) -> bool:
    """
    Check if the path is for a .py file that satisfies the include and exclude patterns.
    """
    if path.suffix != ".py":
        return False
    name = _relative_filename(path, repo)
    if include and not any(fnmatch(name, pattern) for pattern in include):
        return False
    if exclude and any(fnmatch(name, pattern) for pattern in exclude):
        return False
    return True


class _StatusGroups(NamedTuple):
    new: list[PythonNode]
    synced: list[PythonNode]
    updated_document: list[PythonNode]
    updated_metadata: list[PythonNode]


def _group_by_status(
    nodes: list[PythonNode], nodes_in_db: PythonNodeMetadatas
) -> _StatusGroups:
    """
    Group nodes by their change status relative to the nodes in the database.
    """
    new: list[PythonNode] = []
    synced: list[PythonNode] = []
    updated_document: list[PythonNode] = []
    updated_metadata: list[PythonNode] = []

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


def _describe_nodes(nodes: list[PythonNode] | list[str], description: str) -> None:
    """Print a status for a group of nodes."""
    LOG.info(f"{len(nodes)} nodes {description}")
    for node in nodes:
        LOG.debug(f" - {node.id if isinstance(node, PythonNode) else node}")


def _get_ids_to_delete(
    nodes_seen: list[PythonNode],
    nodes_in_db: PythonNodeMetadatas,
    repo: Path,
    include: list[str],
    exclude: list[str],
) -> set[str]:
    """
    Return the ids for nodes that should be deleted from the vector database.
    This only applies to nodes that satisfy the filepath filters BUT
    which are not present in the generated nodes.
    """
    ids_seen = {node.id for node in nodes_seen}
    return {
        id
        for id in nodes_in_db
        if id not in ids_seen
        and _is_valid_path(Path(nodes_in_db[id]["file"]), repo, include, exclude)
    }


if __name__ == "__main__":
    import sys

    sys.exit(main())
