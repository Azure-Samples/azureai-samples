# Use the OpenAI Python SDK with Azure AI Agent service

In addition to the AI Agent SDK, you can also use the Azure AI Agent service with the OpenAPI SDK. This can be useful if you're an existing Azure OpenAI Assistants customer, and have applications that already utilize the OpenAPI SDK. See the following examples for more information.

## Basic example

> [!TIP]
> You can find a streaming example in the Azure Python SDK repo on [Github](https://github.com/Azure/azure-sdk-for-python/blob/jhakulin/oai-agents/sdk/ai/azure-ai-projects/samples/agents/sample_openai_assistants_streaming.py).

```python
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI


with AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
) as project_client:

    # Explicit type hinting for IntelliSense
    client: AzureOpenAI = project_client.inference.get_azure_openai_client()

    with client:
        agent = client.beta.assistants.create(
            model="gpt-4o-mini", name="my-agent", instructions="You are a helpful agent"
        )
        print(f"Created agent, agent ID: {agent.id}")

        thread = client.beta.threads.create()
        print(f"Created thread, thread ID: {thread.id}")

        message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content="Hello, tell me a joke")
        print(f"Created message, message ID: {message.id}")

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=agent.id)

        # Poll the run while run status is queued or in progress
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)  # Wait for a second
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Run status: {run.status}")

        client.beta.assistants.delete(agent.id)
        print("Deleted agent")

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(f"Messages: {messages}")
```



## Function calling

> [!TIP]
> You can find a streaming example in the Azure Python SDK repo on [Github](https://github.com/Azure/azure-sdk-for-python/blob/jhakulin/oai-agents/sdk/ai/azure-ai-projects/samples/agents/sample_openai_assistants_streaming_functions.py).

```python
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from openai.types.beta.threads.required_action_function_tool_call import RequiredActionFunctionToolCall
from azure.ai.projects.models import FunctionTool
from user_functions import user_functions


with AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
) as project_client:

    # Explicit type hinting for IntelliSense
    client: AzureOpenAI = project_client.inference.get_azure_openai_client()

    # Initialize function tool with user functions
    functions = FunctionTool(functions=user_functions)

    with client:
        agent = client.beta.assistants.create(
            model="gpt-4o-mini", name="my-agent", instructions="You are a helpful agent", tools=functions.definitions
        )
        print(f"Created agent, agent ID: {agent.id}")

        thread = client.beta.threads.create()
        print(f"Created thread, thread ID: {thread.id}")

        message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content="Hello, send an email with the datetime and weather information in New York?")
        print(f"Created message, message ID: {message.id}")

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=agent.id)

        # Poll the run while run status is queued or in progress
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)  # Wait for a second
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Run status: {run.status}")

            if run.status == "requires_action" and run.required_action is not None:

                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    client.beta.threads.runs.cancel(thread_id=thread.id, run_id=run.id)
                    break

                tool_outputs = []
                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredActionFunctionToolCall):
                        try:
                            output = functions.execute(tool_call)
                            tool_outputs.append(
                                {
                                    "tool_call_id": tool_call.id,
                                    "output": output,
                                }
                            )
                        except Exception as e:
                            print(f"Error executing tool_call {tool_call.id}: {e}")

                print(f"Tool outputs: {tool_outputs}")
                if tool_outputs:
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )

        client.beta.assistants.delete(agent.id)
        print("Deleted agent")

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(f"Messages: {messages}")
```


## File search 

```python    
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from azure.ai.projects.models import FileSearchTool


with AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
) as project_client:

    # Explicit type hinting for IntelliSense
    client: AzureOpenAI = project_client.inference.get_azure_openai_client()

    openai_file = client.files.create(file=open("product_info_1.md", "rb"), purpose="assistants")
    print(f"Uploaded file, file ID: {openai_file.id}")

    # Create vector store with file, note: there is no poll method to check the status of vector store is ready
    openai_vectorstore = client.beta.vector_stores.create(file_ids=[openai_file.id], name="my_vectorstore")

    # poll the vector store status, the vector store status can be "in_progress", "completed", "expired"
    # status can be get from client.beta.vector_stores.retrieve(openai_vectorstore.id)
    while openai_vectorstore.status == "in_progress":
        time.sleep(1)
        openai_vectorstore = client.beta.vector_stores.retrieve(openai_vectorstore.id)

    print(f"Created vector store, vector store ID: {openai_vectorstore.id}")

    # Create file search tool with resources
    file_search = FileSearchTool(vector_store_ids=[openai_vectorstore.id])

    with client:
        agent = client.beta.assistants.create(
            model="gpt-4o-mini", name="my-agent", instructions="You are a helpful agent", tools=file_search.definitions, tool_resources=file_search.resources
        )
        print(f"Created agent, agent ID: {agent.id}")

        thread = client.beta.threads.create()
        print(f"Created thread, thread ID: {thread.id}")

        message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?")
        print(f"Created message, message ID: {message.id}")

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=agent.id)

        # Poll the run while run status is queued or in progress
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)  # Wait for a second
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Run status: {run.status}")

        if run.status == "failed":
            # Check if you got "Rate limit is exceeded.", then you want to get more quota
            print(f"Run failed: {run.last_error}")

        client.beta.vector_stores.delete(openai_vectorstore.id)
        print("Deleted vector store")

        client.beta.assistants.delete(agent.id)
        print("Deleted agent")

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(f"Messages: {messages}")
```
