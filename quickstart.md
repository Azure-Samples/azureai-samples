# AI Agents Quick Start 

This QuickStart demonstrates how to quickly set up your first agent with Azure AI Agent Service. 
 
## Complete Azure prerequisites 

1. Create an Azure Subscription for [free](https://azure.microsoft.com/free/ai-services/), if you don't have one already. 

1. Make sure both developers and end users have the following permissions: 

    * `Microsoft.MachineLearningServices/workspaces/agents/read` 
    * `Microsoft.MachineLearningServices/workspaces/agents/action` 
    * `Microsoft.MachineLearningServices/workspaces/agents/delete` 

    If you want to create custom permissions, make sure they have: 

    `agents/*/read` 

    `agents/*/action` 

    `agents/*/delete` 

## Setup your Azure AI Hub and Agent project 

To set up an [Azure AI hub and project](https://learn.microsoft.com/azure/ai-studio/quickstarts/get-started-playground): 

1. Create an Azure AI Hub to set up your app environment and network HOBO resources  

1. Create an Azure AI project under your Hub to provides an endpoint for your app to call, and set up proxy app services to access to resources in your tenant.  

1. Connect an Azure OpenAI resource or an Azure AI resource 

Follow these steps to set up your hub and project: 

1. Install [the Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli-windows?tabs=azure-cli). If you have the CLI already installed, make sure it's updated to the latest version.

1. Register a provider. 
    
    ```console
    az provider register –namespace  {my_resource_namespace} 
    
                         [--accept-terms] 
    
                         [--consent-to-permissions] 
    
                         [--management-group-id] 
    
                         [--wait] 
    ```

1. To authenticate to your Azure subscription from the Azure CLI, use the following command: 

    ```console
    az login
    ```
2. Create a resource group: 

    ```console
    az group create --name {my_resource_group} --location westus2 
    ```

  

1. Create an Azure OpenAI resource: 

    > [!NOTE]
    > Azure AI Agent Service is currently available for all OpenAI models in available Azure Regions (see the [models guide](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)) and Llama 3.1-405B-instruct. We will be expanding to more models in the future. 

    ```
    az cognitiveservices account create --name {my-multi-service-resource} --resource-group {my_resource_group} --kind AIServices --sku s0 --location westus2  
    ```
  

    Alternatively, you can create an AI Services resource: 
    
    ```console
    az cognitiveservices account create --name {MyOpenAIResource} --resource-group {my_resource_group} --location westus2 --kind OpenAI --sku s0  
    ```
  

    Save the id that gets output, you’ll need it later. It will look similar to: `https://eastus.api.cognitive.microsoft.com/ai_services_resource_id: /subscriptions/1234-5678-abcd-9fc6-62780b3d3e05/resourceGroups/my-resource-group/providers/Microsoft.CognitiveServices/accounts/multi-service-resource` 

1. Create a Bing grounding resource.
 
    ```console
    az cognitiveservices account create \ 
    
      --name bing-grounding-resource \ 
    
      --resource-group <resource-group-name> \ 
    
      --kind Bing.Grounding \ 
    
      --sku G1 \ 
    
      --location Global \ 
    
      --yes 
    ```

1. Create an Azure AI Hub.  

    > [!NOTE] the following command auto creates a storage account, AML workspace and Key Vault. 

    ```console
    az ml workspace create --kind hub --resource-group {my_resource_group} --name {my_hub_name} 
    ```

    OR 

    Optional: If you want to connect an existing storage account and/or key vault you can specify them here: 

    ```console
    az ml workspace create --kind hub --resource-group {my_resource_group} --name {my_hub_name} --location {hub-region} --storage-account {my_storage_account_id} --key-vault {my_key_vault_id} 
    ```
 
1. Connect your Hub to your Azure AI resource or Azure OpenAI resource. Replace the resource group and hub name with your resource and hub name. 

    1. Save the following in a file named `connection.yml`.

    1. If using an AI Services resource, use the following and replace ai_services_resource_id with the fully qualified ID from earlier.   

    ```yml
    name: myazai_connection  
    type: azure_ai_services  
    endpoint: https://eastus.api.cognitive.microsoft.com/  
    ai_services_resource_id: /subscriptions/12345678-abcd-1234-9fc6-62780b3d3e05/resourceGroups/my-ai-resource-group/providers/Microsoft.CognitiveServices/accounts/multi-service-resource 
    ```

    1. If using an Azure OpenAI resource, create the following `connection.yml` file: 
    ```yml
    name: {my_connection_name} 
    type: azure_open_ai 
    azure_endpoint: https://eastus.api.cognitive.microsoft.com/ 
    ```
 

1. Then run the following command: 

    ```console
    az ml connection create --file connection.yml --resource-group {my_resource_group} --workspace-name {my_hub_name}  
    ```

1. Create a Project.  

    1. Run the following command to find your ARM Template: 

    ```console
    az ml workspace show -n {my_hub_name} --resource-group {my_resource_group} --query id 
    ```

    1. Now run this command to create your project 

    ```console
    az ml workspace create --kind project --hub-id {my_hub_ARM_ID} --resource-group {my_resource_group} --name {my_project_name} 
    ```

## Configure and run your first agent


| Component | Description |
|---|---|
| Agent | Custom AI that uses AI models in conjunction with tools. |
| Tool | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information. |
| Thread | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context. | 
| Message | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread. |
| Run | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. 
| Run Step | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results. |

Use the following code to create an agent and send a message to it. This agent will have the code interpreter  tool to enable your agent to perform advanced data analysis in a sandboxed environment and Bing search tool  to real-time, web data grounding. 

## Python SDK

> [!NOTE]
> You can find [C# code below](#c).

Run the following command to install the python package. 

```console
python -m pip install azure-ai-projects azure-identity 
```

Use the following code to create and run an agent.

```python
import os  
from azure.ai.projects import AIProjectClient  
from azure.ai.projects.models import Agent, MessageDeltaChunk, MessageDeltaTextContent, RunStep, ThreadMessage, ThreadRun  
from azure.ai.projects.models import AgentEventHandler  
from azure.ai.projects.operations import AgentsOperations  
from azure.identity import DefaultAzureCredential  
from azure.ai.projects.models import CodeInterpreterTool, bing_grounding, ToolSet  
from typing import Any  

# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

# When using CodeInterpreterTool with ToolSet in agent creation, the tool call events are handled inside the create_stream
# method and functions gets automatically called by default.
class MyEventHandler(AgentEventHandler):

    def on_message_delta(self, delta: "MessageDeltaChunk") -> None:
        for content_part in delta.delta.content:
            if isinstance(content_part, MessageDeltaTextContent):
                text_value = content_part.text.value if content_part.text else "No text"
                print(f"Text delta received: {text_value}")

    def on_thread_message(self, message: "ThreadMessage") -> None:
        print(f"ThreadMessage created. ID: {message.id}, Status: {message.status}")

    def on_thread_run(self, run: "ThreadRun") -> None:
        print(f"ThreadRun status: {run.status}")

        if run.status == "failed":
            print(f"Run failed. Error: {run.last_error}")

    def on_run_step(self, step: "RunStep") -> None:
        print(f"RunStep type: {step.type}, Status: {step.status}")

    def on_error(self, data: str) -> None:
        print(f"An error occurred. Data: {data}")

    def on_done(self) -> None:
        print("Stream completed.")

    def on_unhandled_event(self, event_type: str, event_data: Any) -> None:
        print(f"Unhandled Event Type: {event_type}, Data: {event_data}")

# create a connection to the grounding with bing search resource
connection_name = "bing_grounding_connection"
target = "GROUNDING_WITH_BING_SEARCH_API"
wps_connection = WorkspaceConnection(
    name=connection_name,
    type="custom",
    target=target,
    credentials=ApiKeyConfiguration(key="API_KEY"),
)
ml_client.connections.create_or_update(workspace_connection=wps_connection)

with project_client:
    # Create Grounding with Bing Search tool with resources
    bing_grounding_tool = bing_grounding(connection_id=[connection id of Grounding with Bing Search resource])
    code_interpreter = CodeInterpreterTool()
    toolset = ToolSet()
    toolset.add(code_interpreter)
    toolset.add(bing_grounding_tool)

    agent = project_client.agents.create_agent(
        model="gpt-4-1106-preview", name="my-assistant", instructions="You are a helpful assistant", toolset=toolset
    )
    print(f"Created agent, ID: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Write code to calculate compound interest.",
    )
    print(f"Created message, message ID {message.id}")

    with project_client.agents.create_stream(
        thread_id=thread.id, assistant_id=agent.id, event_handler=MyEventHandler()
    ) as stream:
        stream.until_done()

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
```

## C#