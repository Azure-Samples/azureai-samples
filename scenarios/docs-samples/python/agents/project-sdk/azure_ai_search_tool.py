"""
DESCRIPTION:
    This sample demonstrates how to use agent operations with the 
    Azure AI Search tool from the Azure Agents service using a synchronous client.

PREREQUISITES:
    You will need an Azure AI Search Resource. 
    If you already have one, you must create an agent that can use an existing Azure AI Search index:
    https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/azure-ai-search?tabs=azurecli%2Cpython&pivots=overview-azure-ai-search
    
    If you do not already have an Agent Setup with an Azure AI Search resource, follow the guide for a Standard Agent setup: 
    https://learn.microsoft.com/azure/ai-services/agents/quickstart?pivots=programming-language-python-azure

USAGE:
    python azure_ai_search_tool.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
    3) AI_SEARCH_CONNECTION_NAME - The connection name of the AI Search connection to your Foundry project,
       as found under the "Name" column in the "Connected Resources" tab in your Azure AI Foundry project.
"""
# <create a project client>
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AzureAISearchTool, AzureAISearchQueryType, ListSortOrder, MessageRole
from azure.identity import DefaultAzureCredential

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;my-subscription-id;my-resource-group;my-hub-name

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)
# </create a project client>

# <get azure ai search connection_id>
# Get the connection ID of your Azure AI Search resource
connection = project_client.connections.get(connection_name=os.environ["AI_SEARCH_CONNECTION_NAME"])
conn_id = connection.id

print(conn_id)
# </get azure ai search connection_id>


# <configure the azure ai search tool>
# Initialize agent AI search tool and add the search index connection ID and index name
# TO DO: replace <your-index-name> with the name of the index you want to use
ai_search = AzureAISearchTool(
    index_connection_id=conn_id,
    index_name="<your-index-name>",
    query_type=AzureAISearchQueryType.VECTOR_SIMPLE_HYBRID,
    top_k=3,
    # filter=""
)
# </configure the azure ai search tool>

# <create agent>
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-assistant",
    instructions="You are a helpful assistant",
    tools=ai_search.definitions,
    tool_resources=ai_search.resources,
)

print(f"Created agent, ID: {agent.id}")
# </create agent>

# <create thread and run>
# Create thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="What is the temperature rating of the cozynights sleeping bag?",
)
print(f"Created message, ID: {message.id}")

# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch run steps to get the details of the agent run
run_steps = project_client.agents.list_run_steps(thread_id=thread.id, run_id=run.id)
for step in run_steps.data:
    print(f"Step {step['id']} status: {step['status']}")
    step_details = step.get("step_details", {})
    tool_calls = step_details.get("tool_calls", [])

    if tool_calls:
        print("  Tool calls:")
        for call in tool_calls:
            print(f"    Tool Call ID: {call.get('id')}")
            print(f"    Type: {call.get('type')}")

            azure_ai_search_details = call.get("azure_ai_search", {})
            if azure_ai_search_details:
                print(f"    azure_ai_search input: {azure_ai_search_details.get('input')}")
                print(f"    azure_ai_search output: {azure_ai_search_details.get('output')}")
    print()  # add an extra newline between steps

# Delete the assistant when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages.data:
    if message.role == MessageRole.AGENT and message.url_citation_annotations:
        placeholder_annotations = {
            annotation.text: f" [see {annotation.url_citation.title}] ({annotation.url_citation.url})"
            for annotation in message.url_citation_annotations
        }
        for message_text in message.text_messages:
            message_str = message_text.text.value
            for k, v in placeholder_annotations.items():
                message_str = message_str.replace(k, v)
            print(f"{message.role}: {message_str}")
    else:
        for message_text in message.text_messages:
            print(f"{message.role}: {message_text.text.value}")
# <create thread and run>
