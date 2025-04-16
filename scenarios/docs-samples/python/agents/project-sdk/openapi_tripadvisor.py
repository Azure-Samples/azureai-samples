# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
FILE: openapi_tripadvisor.py
DESCRIPTION:
    This sample demonstrates how to use agent operations to retrieve licensed data from Tripadvisor. To learn more about the set up, please visit: https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/licensed-data
USAGE:
    python sample_agents_openapi.py
    Before running the sample:
    pip install azure-ai-projects azure-identity jsonref
    Set this environment variables with your own values:
    PROJECT_CONNECTION_STRING - the Azure AI Project connection string, as found in your AI Studio Project.
"""

import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme, OpenApiAnonymousAuthDetails


# Create an Azure AI Client from a connection string, copied from your AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="PROJECT_CONNECTION_STRING",  # Replace with your actual connection string
)

with open('./tripadvisor.json', 'r') as f:
    openapi_spec = jsonref.loads(f.read())

tripadvisor_connection = project_client.connections.get(
    connection_name="CONNECTION_NAME"  # Replace with your actual connection name
)
conn_id = tripadvisor_connection.id
print(conn_id)

auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=conn_id))
openapi = OpenApiTool(name="tripadvisor", spec=openapi_spec, description="get hotel and restaurant reviews of a location", auth=auth)

# Create agent with OpenApi tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-assistant",
        instructions="You are a helpful travel planning agent. Please use Tripadvisor to find recommendations and reviews for hotels, restaurants and more.",
        tools=openapi.definitions
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="top 5 hotels in Paris, France and their review links",
    )
    print(f"Created message, ID: {message.id}")

    # Create and process agent run in thread with tools
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")


    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the assistant when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")