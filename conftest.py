import json
import types
from pathlib import Path
from typing import Dict

import pytest

REPO_ROOT = Path(__file__).parent.resolve()


@pytest.fixture
def notebook_path(
    # Create and activate a new venv for each test that requests `notebook_path`
    venv: types.SimpleNamespace,  # noqa: ARG001
    notebook_path: Path,
) -> Path:
    """Activates a virtual environment for tests that request notebook_path (Jupyter Notebook tests)."""
    return notebook_path


@pytest.fixture
def deployment_outputs() -> Dict[str, str]:
    """The outputs of the deployment used to setup resources for testing samples.

    Depends on the existence of a `deployment.json` file in the root of the repository,
    which is the output of running `az deployment sub create -o json`
    """
    deployment_file_path = REPO_ROOT / "deployment.json"

    try:
        with deployment_file_path.open() as f:
            deployment = json.load(f)
    except (FileExistsError, json.JSONDecodeError) as e:
        raise AssertionError("Please use azure-cli to perform a deployment and same result to deployment.json") from e

    properties = deployment.get("properties")

    if properties is None or "outputs" not in properties:
        raise AssertionError("Key 'properties.outputs' not present in deployment json")

    outputs = properties.get("outputs")

    return {output_name: output["value"] for output_name, output in outputs.items()}


@pytest.fixture
def azure_ai_project(deployment_outputs: Dict[str, str]) -> Dict[str, str]:
    """Azure ai project dictionary."""
    return {
        "subscription_id": deployment_outputs["subscription_id"],
        "resource_group_name": deployment_outputs["resource_group_name"],
        "project_name": deployment_outputs["project_name"],
    }


@pytest.fixture
def azure_ai_project_connection_string(deployment_outputs: Dict[str, str]) -> str:
    """The connection string for the azure ai project"""
    return ";".join(
        [
            f"{deployment_outputs['project_location']}.api.azureml.ms",
            deployment_outputs["subscription_id"],
            deployment_outputs["resource_group_name"],
            deployment_outputs["project_name"],
        ]
    )


@pytest.fixture
def azure_openai_endpoint(deployment_outputs: Dict[str, str]) -> str:
    """The azure openai endpoint for the azure ai project."""
    return deployment_outputs["azure_openai_endpoint"]


@pytest.fixture
def azure_openai_gpt4_deployment(deployment_outputs: Dict[str, str]) -> str:
    """The deployment name of the gpt-4 deployment."""
    return deployment_outputs["azure_openai_gpt4_deployment_name"]


@pytest.fixture
def azure_openai_gpt4_api_version(deployment_outputs: Dict[str, str]) -> str:
    """The api version of the gpt-4 deployment."""
    return deployment_outputs["azure_openai_gpt4_api_version"]
