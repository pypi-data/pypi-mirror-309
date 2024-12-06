import argparse
import logging
from pathlib import Path
from typing import Literal, Sequence


from python_embeddings.git_utils import git_repo_name

from python_embeddings.vector_db import (
    default_client,
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
        "-q",
        "--query",
        type=str,
        nargs="+",
        help="Query the vector database for semantic similarity to the given query",
    )
    parser.add_argument(
        "-n",
        "--n_results",
        type=int,
        default=10,
        help="The max number of results to return",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print debug messages",
    )

    try:
        args = parser.parse_args(argv)
        repo = Path(args.repo).resolve()
        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.INFO,
            format="%(asctime)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        client = default_client()
        collection_name = args.collection or git_repo_name(repo)
        collection = client.get_or_create_collection(collection_name)
        result = collection.query(query_texts=args.query, n_results=args.n_results)
        LOG.info(f"Found {len(result)} results")
        LOG.info(result)
        # sync(
        #     repo=repo,
        #     client=default_client(),
        #     collection_name=args.collection or git_repo_name(repo),
        #     include=args.include or [],
        #     exclude=args.exclude or [],
        #     delete=args.delete,
        #     dry_run=args.dry_run,
        # )
        LOG.info("Search complete")
        return 0

    except Exception:
        LOG.exception("An error occurred")
        return 1


# def sync(
#     repo: Path,
#     client: ClientAPI,
#     collection_name: str,
#     include: list[str],
#     exclude: list[str],
#     delete: bool,
#     dry_run: bool,
# ) -> None:
#     """
#     Sync the python code in a git repository with a vector database.
#     """
#     embedding_function = default_embedding_function()
#     assert embedding_function is not None, "No embedding function found"

#     collection = client.get_or_create_collection(collection_name)

#     nodes_seen: list[PythonNode] = []

#     nodes_in_db = get_metadatas(collection)
#     files_in_db = {metadata["file"] for metadata in nodes_in_db.values()}
#     LOG.info(f"{len(files_in_db)} files currently exist in '{collection_name}'")
#     LOG.info(f"{len(nodes_in_db)} nodes currently exist in '{collection_name}'")

#     files = _get_python_files(repo, include, exclude)
#     LOG.info(f"{len(files)} python files will be parsed")

#     for path in tqdm(files, desc="Parsing files"):
#         LOG.info(f"{path.relative_to(repo)}")

#         with log_message_prefix("\t"):
#             nodes = parse_python_module(path, repo)
#             LOG.info(f"Extracted {len(nodes)} nodes")

#             nodes_seen.extend(nodes)

#             status = _group_by_status(nodes, nodes_in_db)

#             if dry_run:
#                 _describe_nodes(status.synced, "are synced")
#                 _describe_nodes(status.new, "will be created")
#                 _describe_nodes(status.updated_document, "will be updated")
#                 _describe_nodes(
#                     status.updated_metadata, "will have their metadata updated"
#                 )
#             else:
#                 _describe_nodes(status.synced, "are synced")
#                 add_nodes(collection, embedding_function, status.new)
#                 update_nodes(collection, embedding_function, status.updated_document)
#                 update_metadatas(collection, status.updated_metadata)

#     if delete:
#         ids = _get_ids_to_delete(nodes_seen, nodes_in_db, repo, include, exclude)
#         if ids:
#             if dry_run:
#                 _describe_nodes(list(ids), "will be deleted")
#             else:
#                 delete_nodes(collection, ids)
