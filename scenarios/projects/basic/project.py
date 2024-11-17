from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_connection_string = "your_connection_string"

project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential()
)
