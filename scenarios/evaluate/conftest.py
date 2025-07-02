from typing import Any, Dict

import pytest


@pytest.fixture
def papermill_parameters(
    azure_ai_project: Dict[str, str],
    azure_ai_project_connection_string: str,
    azure_openai_gpt4_deployment: str,
    azure_openai_endpoint: str,
    azure_openai_gpt4_api_version: str,
) -> Dict[str, Any]:
    return {
        "azure_ai_connection_string": azure_ai_project_connection_string,
        "azure_ai_project": azure_ai_project,
        "azure_openai_endpoint": azure_openai_endpoint,
        "azure_openai_deployment": azure_openai_gpt4_deployment,
        "azure_openai_api_version": azure_openai_gpt4_api_version,
    }
