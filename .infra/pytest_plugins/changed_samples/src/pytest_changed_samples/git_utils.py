from pathlib import Path
from typing import Iterable, Optional

from git import Repo


def get_diff_paths(a: str, b: Optional[str]) -> Iterable[Path]:
    """Get a list of paths that have changed between two git refs

    :param str a: The base ref to diff against
    :param Optional[str] b: The ending ref to diff against. If "None",
        will diff against the working tree
    :returns: The list of paths
    :rtype: Iterable[Path]
    """
    repo = Repo(search_parent_directories=True)
    repo_path = Path(repo.working_dir).resolve()

    # Diffs that are either in the working tree or staged in the index
    changed_files = repo.commit(a).diff(b)

    for c in changed_files:
        for p in {c.a_path, c.b_path}:
            if p is None:
                continue

            yield Path(repo_path, p).resolve()


def get_all_modified_paths() -> Iterable[Path]:
    """Get paths to all non-committed changes tracked by git

    This list includes files in the working tree and staged in the index

    :returns: List of changed paths
    :rtype: Iterable[Path]
    """
    return get_diff_paths("HEAD", None)


def get_branch_diff_paths(ref: str = "main") -> Iterable[Path]:
    """Get a list of all paths changed between HEAD and the main branch

    :returns: List of changed paths
    :rtype: Iterable[Path]
    """
    return get_diff_paths("HEAD", ref)
