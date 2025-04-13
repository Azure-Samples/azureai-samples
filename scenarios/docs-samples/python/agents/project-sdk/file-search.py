"""
DESCRIPTION:
    This sample demonstrates how to upload files and create a vector store for file search using the Azure Agents service.
    It also demonstrates how to create an agent that can search the vector store and process a message with a file attachment.

USAGE:
    python sample_agents_vector_store_file_search.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
"""

# <create a project client>
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, MessageAttachment, FilePurpose
from azure.identity import DefaultAzureCredential

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

credential = DefaultAzureCredential()
project_client = AIProjectClient.from_connection_string(
    credential=credential, conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)
# </create a project client>

# <upload files and create a vector store>
# We will upload the local file and will use it for vector store creation.

# upload a file
file = project_client.agents.upload_file_and_poll(file_path="./data/product_catelog.md", purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {file.id}")

# create a vector store with the file you uploaded
vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
print(f"Created vector store, vector store ID: {vector_store.id}")
# </upload files and create a vector store>

# <create agent>
# create a file search tool
file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

# notices that FileSearchTool as tool and tool_resources must be added or the agent will be unable to search the file
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are a helpful agent",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)
print(f"Created agent, agent ID: {agent.id}")
# </create agent>

# <create thread>
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

# Upload the user provided file as a messsage attachment
message_file = project_client.agents.upload_file_and_poll(file_path="product_info_1.md", purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {message_file.id}")

# Create a message with the file search attachment
# Notice that vector store is created temporarily when using attachments with a default expiration policy of seven days.
attachment = MessageAttachment(file_id=message_file.id, tools=FileSearchTool().definitions)
message = project_client.agents.create_message(
    thread_id=thread.id, role="user", content="What feature does Smart Eyewear offer?", attachments=[attachment]
)
print(f"Created message, message ID: {message.id}")
# </create thread>

# <create run>
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Created run, run ID: {run.id}")

project_client.agents.delete_vector_store(vector_store.id)
print("Deleted vector store")

project_client.agents.delete_agent(agent.id)
print("Deleted agent")

messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
# </create run>
