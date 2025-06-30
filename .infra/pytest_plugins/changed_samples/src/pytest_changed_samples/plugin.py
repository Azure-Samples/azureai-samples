from pathlib import Path
from typing import Callable, Iterable, Optional

import pytest

from .git_utils import get_all_modified_paths, get_branch_diff_paths
from .trie import Trie

DIFF_PATH_TRIE_KEY = pytest.StashKey[Trie]()
"""A Stash key to a Trie that stores paths to files present in a diff"""

WORKING_TREE_CHANGES_OPTION = "--changed-samples-only"
PR_CHANGES_OPTION = "--changed-samples-only-from"


def is_plugin_active(config: pytest.Config) -> bool:
    """Return whether any of the plugin provided options were provided on commandline."""
    return get_diff_paths_function(config) is not None


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        WORKING_TREE_CHANGES_OPTION,
        action="store_true",
        help=(
            "Only collect tests for samples that have changed relative to the last commit (HEAD)."
            + " A sample has 'changed' if any file in its parent directory has been modified."
        ),
    )

    parser.addoption(
        PR_CHANGES_OPTION,
        action="store",
        help=(
            "Only collect tests for samples that have changed relative to the specified git ref."
            + " A sample has 'changed' if any file in its parent directory has been modified."
        ),
    )


def pytest_configure(config: pytest.Config) -> None:
    # Validate that mutually exclusive options haven't been provided
    mutually_exclusive_options = (WORKING_TREE_CHANGES_OPTION, PR_CHANGES_OPTION)
    if sum(bool(config.getoption(opt_var(o))) for o in mutually_exclusive_options) > 1:
        raise pytest.UsageError(f"{' and '.join(mutually_exclusive_options)} are mutually exclusive")


@pytest.hookimpl(hookwrapper=True)
def pytest_collection(session: pytest.Session) -> None:
    """Set up path filtering based on git diff."""
    config = session.config
    diff_path_trie = Trie()

    paths_filter = get_diff_paths_function(config)

    if paths_filter is None:
        # Exit early if there's no path filter
        yield
        return

    for p in paths_filter():
        diff_path_trie.insert(p.parts)

    config.stash[DIFF_PATH_TRIE_KEY] = diff_path_trie

    yield

    del config.stash[DIFF_PATH_TRIE_KEY]


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> Optional[bool]:
    """Ignore paths that were not touched by the current git diff."""
    if DIFF_PATH_TRIE_KEY not in config.stash:
        # Occurs when calling `pytest --fixtures`
        return None

    diff_path_trie = config.stash[DIFF_PATH_TRIE_KEY]

    # NOOP if diff is empty
    if len(diff_path_trie) == 0:
        return None

    ignore_dir = collection_path if collection_path.is_dir() else collection_path.parent

    # Either definitely ignore this path, or defer decision to other plugins
    return (not diff_path_trie.is_prefix(ignore_dir.resolve().parts)) or None


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if not is_plugin_active(session.config):
        return

    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK


def get_diff_paths_function(config: pytest.Config) -> Optional[Callable[[], Iterable[Path]]]:
    """Get the function that returns paths present in a diff specfied by cmdline arguments

    :param pytest.Config config: The pytest config
    :returns: A function that returns one of:
        * Paths to files that have changed between HEAD and the working tree
        * Paths to files that have changed between HEAD and main
        * No paths
    :rtype: Callable[[],Iterable[Path]]
    """
    if config.getoption(opt_var(WORKING_TREE_CHANGES_OPTION)):
        return get_all_modified_paths
    if ref := config.getoption(opt_var(PR_CHANGES_OPTION)):
        return lambda: get_branch_diff_paths(ref)

    return None


def opt_var(s: str) -> str:
    """Return the name of the variable associated with a given commandline option

    :param str s: A string in the form of a commandline option (e.g. `--hello-world`)
    :returns: The variable associated with the commandline option (e.g. `hello_world`)
    :rtype: str
    """
    return s.lstrip("-").replace("-", "_")
