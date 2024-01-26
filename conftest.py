import types
from pathlib import Path
from typing import Dict

import pytest
from dotenv import dotenv_values


@pytest.fixture()
def notebook_path(
    # Create a new venv for each test that requests `notebook_path`
    venv: types.SimpleNamespace,  # noqa: ARG001
    notebook_path: Path,
) -> Path:
    return notebook_path


@pytest.fixture()
def dotenv() -> Dict[str, str]:
    return dotenv_values(Path(__file__).parent / ".env")
