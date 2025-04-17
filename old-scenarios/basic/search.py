# ruff: noqa: E402

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# <get_search_client>
from azure.core.credentials import AzureKeyCredential
from azure.ai.projects.models import ConnectionType
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

# use the project client to get the default search connection
search_connection = project.connections.get_default(
    connection_type=ConnectionType.AZURE_AI_SEARCH, include_credentials=True
)

# Create a client to create and manage search indexes
index_client = SearchIndexClient(
    endpoint=search_connection.endpoint_url, credential=AzureKeyCredential(key=search_connection.key)
)

# Create a client to run search queries
search_client = SearchClient(
    index_name="your_index_name",
    endpoint=search_connection.endpoint_url,
    credential=AzureKeyCredential(key=search_connection.key),
)
# </get_search_client>
