# AI Agents Quick Start 

This QuickStart demonstrates how to quickly set up your first agent with Azure AI Agent Service. 
 
## Complete Azure prerequisites 

1. Create an Azure Subscription for [free](https://azure.microsoft.com/free/ai-services/), if you don't have one already. 

1. check the [RBAC roles](./rbac.md). 

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

## Install the SDK package

Depending on your programming language of choice install the SDK using the following steps:

### Python

1. Download the [Python .whl file](./packages/azure_ai_project-1.0.0b1-py3-none-any.whl) to your project directory.
1. Install the SDK with `pip install azure_ai_project-1.0.0b1-py3-none-any.whl --user --force-reinstall`
    >[!NOTE]
    > We recommend creating a virtual environment with [venv](https://docs.python.org/3/library/venv.html).

### C#

TBD

## Configure and run your first agent


| Component | Description |
|---|---|
| Agent | Custom AI that uses AI models in conjunction with tools. |
| Tool | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information. |
| Thread | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context. | 
| Message | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread. |
| Run | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. 
| Run Step | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results. |

Use the following code to create an agent and send a message to it. This agent will have the code interpreter  tool to enable your agent to perform advanced data analysis in a sandboxed environment. 

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
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import FilePurpose
from azure.identity import DefaultAzureCredential
from pathlib import Path

# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:

    code_interpreter = CodeInterpreterTool(file_ids=[file.id])

    # notice that CodeInterpreter must be enabled in the agent creation, otherwise the agent will not be able to see the file attachment
    agent = project_client.agents.create_agent(
        model="gpt-4-1106-preview",
        name="my-agent",
        instructions="You are a helpful agent",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9.",
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    messages = project_client.agents.get_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    last_msg = messages.get_last_text_message_by_sender("assistant")
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")

    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")

    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")

    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## C#

Use the following package in your C# project 

```console
dotnet add package Azure.AI.Project --prerelease 
```

Then use the following sample code to create an agent.

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Identity;
using NUnit.Framework;

namespace Azure.AI.Projects.Tests
{
    public class Sample_Agent_Streaming
    {
        public async Task Streaming()
        {
            var connectionString = Environment.GetEnvironmentVariable("AZURE_AI_CONNECTION_STRING");
            AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());

            Response<Agent> agentResponse = await client.CreateAgentAsync(
                model: "gpt-4-1106-preview",
                name: "My Friendly Test Agent",
                instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
                tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() });
            Agent agent = agentResponse.Value;

            Response<AgentThread> threadResponse = await client.CreateThreadAsync();
            AgentThread thread = threadResponse.Value;

            Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
                thread.Id,
                MessageRole.User,
                "Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9.");
            ThreadMessage message = messageResponse.Value;

            await foreach (StreamingUpdate streamingUpdate in client.CreateRunStreamingAsync(thread.Id, agent.Id))
            {
                if (streamingUpdate.UpdateKind == StreamingUpdateReason.RunCreated)
                {
                    Console.WriteLine($"--- Run started! ---");
                }
                else if (streamingUpdate is MessageContentUpdate contentUpdate)
                {
                    Console.Write(contentUpdate.Text);
                    if (contentUpdate.ImageFileId is not null)
                    {
                        Console.WriteLine($"[Image content file ID: {contentUpdate.ImageFileId}");
                    }
                }
            }
        }
    }
}
```
