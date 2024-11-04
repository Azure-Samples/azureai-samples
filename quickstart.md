# AI Agents Quick Start 

This QuickStart demonstrates how to quickly set up your first agent with Azure AI Agent Service. 
 
## Complete Azure prerequisites 

1. Create an Azure Subscription for [free](https://azure.microsoft.com/free/ai-services/), if you don't have one already. 

1. check the [RBAC roles](./rbac.md). 

## Setup your Azure AI Hub and Agent project 

TThe following section will show you how to set up an [Azure AI hub and project](https://learn.microsoft.com/azure/ai-studio/quickstarts/get-started-playground) by: 

1. Creating an Azure AI Hub to set up your app environment and network HOBO resources  

1. Creating an Azure AI project under your Hub to provides an endpoint for your app to call, and set up proxy app services to access to resources in your tenant.  

1. Connecting an Azure OpenAI resource or an Azure AI resource 

If you already have these resources set up, skip to the [configure and run your first agent section below](#configure-and-run-your-first-agent).

### Follow these steps to set up hub and project: 

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
    az group create --name {my_resource_group} --location westus 
    ```

  

1. Create an Azure OpenAI resource: 

    > [!NOTE]
    > Azure AI Agent Service is currently available for all OpenAI models in available Azure Regions (see the [models guide](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)) and Llama 3.1-405B-instruct. We will be expanding to more models in the future. 

    ```console
     az cognitiveservices account create --name {MyOpenAIResource} --resource-group {my_resource_group} --location westus --kind OpenAI --sku s0
    ```
  

    Alternatively, you can create an AI Services resource: 
    
    ```console
    az cognitiveservices account create --name {my-multi-service-resource} --resource-group {my_resource_group} --kind AIServices --sku s0 --location westus    
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

    1. Run the following command to find your ARM ID: 

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

Use the following code to create an agent and send a message to it. This agent will have the code interpreter  tool to enable your agent to perform advanced data analysis in a sandboxed environment. 

## Python SDK

> [!NOTE]
> You can find [C# code below](#c).

Download the [Python .whl file](./packages/azure_ai_projects-1.0.0b1-py3-none-any.whl) to your project directory.

Run the following commands to install the python packages. 

```console
pip install azure_ai_projects-1.0.0b1-py3-none-any.whl --user --force-reinstall
pip install azure-identity
```

Use the following code to create and run an agent.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any

# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery" 
# To find your HostName, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Create an instance of the CodeInterpreterTool
    code_interpreter = CodeInterpreterTool()
 
    # The CodeInterpeterTool needs to be included in creation of the agent
    agent = project_client.agents.create_agent(
        model="gpt-4-1106-preview",
        name="my-assistant",
        instructions="You are helpful assistant",
        tools=code_interpreter.definitions,
        tool_resources=code_interpreter.resources,
    )
    print(f"Created agent, agent ID: {agent.id}")
    
    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")
 
    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Could you please create a bar chart for the operating profit using the following data and provide the file to me? Company A: $1.2 million, Company B: $2.5 million, Company C: $3.0 million, Company D: $1.8 million",
    )
    print(f"Created message, message ID: {message.id}")
    
    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")
 
    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread 
    messages = project_client.agents.get_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
    
    # Get the last message from the sender
    last_msg = messages.get_last_text_message_by_sender("assistant")
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")
    
    # Generate an image file for the bar chart
    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")
 
    # Print the file path(s) from the messages
    for file_path_annotation in messages.file_path_annotations:
        print(f"File Paths:")
        print(f"Type: {file_path_annotation.type}")
        print(f"Text: {file_path_annotation.text}")
        print(f"File ID: {file_path_annotation.file_path.file_id}")
        print(f"Start Index: {file_path_annotation.start_index}")
        print(f"End Index: {file_path_annotation.end_index}")
    
    # Delete the agent once done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## C#
C# support coming soon!
