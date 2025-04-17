import pytest


@pytest.fixture(autouse=True)
def _skipAll() -> None:
    """Skips all pytest tests in this directory."""
    pytest.skip(reason="Excluded from testing. (Needs to initialize a search index.)")
