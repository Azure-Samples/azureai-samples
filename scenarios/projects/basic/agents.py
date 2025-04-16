# ruff: noqa: E402

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# <create_agent>
from azure.ai.projects.models import FileSearchTool

file = project.agents.upload_file_and_poll(file_path="product_info_1.md", purpose="assistants")
vector_store = project.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
file_search = FileSearchTool(vector_store_ids=[vector_store.id])

# Create agent with file search tool and process the agent run
agent = project.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="Hello, you are helpful agent and can search information from uploaded files",
    tools=file_search.definitions,
    tool_resources=file_search.resources,
)

# </create_agent>

# <run_agent>
# create and run a thread with a message
thread = project.agents.create_thread()
message = project.agents.create_message(
    thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?"
)
run = project.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
if run.status == "failed":
    print(f"Run failed: {run.last_error}")
    exit()

# get messages from the thread and print the response (last message)
messages = project.agents.list_messages(thread_id=thread.id)
for text_message in messages.text_messages:
    print(text_message.as_dict())


# </run_agent>
