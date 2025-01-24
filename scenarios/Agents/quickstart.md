# AI Agents Quick Start

This QuickStart demonstrates how to quickly set up your first agent with Azure AI Agent Service.

## Complete Azure prerequisites

1. Create an Azure Subscription for [free](https://azure.microsoft.com/free/ai-services/), if you don't have one already.

2. Make sure all developers have the role: **Azure AI Developer** assigned at the appropriate level. [Learn more](https://learn.microsoft.com/azure/ai-studio/concepts/rbac-ai-studio)

   If you're using a hub/project that already exists, check the [RBAC roles](./rbac.md).

3. Install [the Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli-windows?tabs=azure-cli). If you have the CLI already installed, make sure it's updated to the latest version.

4. Register providers

   The following providers must be registered:

   - Microsoft.KeyVault
   - Microsoft.CognitiveServices
   - Microsoft.Storage
   - Microsoft.MachineLearningServices
   - Microsoft.Search
   - To use Bing Search tool: Microsoft.Bing

   ```console
   az provider register --namespace 'Microsoft.KeyVault'
   az provider register --namespace 'Microsoft.CognitiveServices'
   az provider register --namespace 'Microsoft.Storage'
   az provider register --namespace 'Microsoft.MachineLearningServices'
   az provider register --namespace 'Microsoft.Search'
   # only to use Grounding with Bing Search tool
   az provider register --namespace 'Microsoft.Bing'
   ```

## Setup your Azure AI Hub and Agent project

The following section will show you how to set up an [Azure AI hub and project](https://learn.microsoft.com/azure/ai-studio/quickstarts/get-started-playground) by:

1. Creating an Azure AI Hub to set up your app environment and Azure resources

1. Creating an Azure AI project under your Hub provisions an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI resource

If you already have these resources set up, skip to the [configure and run your first agent section below](#configure-and-run-your-first-agent).

### Choose Basic, Standard or Network Secured Agent Setup

**Basic Setup** : Agents use multi-tenant search and storage resources fully managed by Microsoft. You won’t have visibility or control over these underlying Azure resources. 
- Resources for the hub, project, storage account, and AI Services will be created for you. The AI Services account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region. A Microsoft-managed key vault will be used by default. 

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you will incur costs based on your usage.
- Resources for the hub, project, storage account, key vault, AI Services, and Azure AI Search will be created for you. The AI Services, AI Search, and Azure Blob Storage account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region.  

**Network Secured Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you will incur costs based on your usage.
- Resources for the hub, project, storage account, key vault, AI Services, and Azure AI Search will be created for you. The AI Services, AI Search, and Azure Blob Storage account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the westus2 region.  
- Customer owned resources will be secured with a provisioned managed network and authenticated with a User Managed Identity with the necessary RBAC permissions. Private links and DNS zones will be created on behalf of customer to ensure network connectivity.



| Template | Description   | Auto-deploy |
| ------------------- | -----------------------------------------------| -----------------------|
|`basic-agent-identity.bicep`| Deploy a basic agent setup that uses Managed Identity authentication on the AI Services/AOAI connection. | [![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fbasic-agent-identity%2Fazuredeploy.json)
| `standard-agent.bicep`  | Deploy a standard agent setup that uses Managed Identity authentication on the AI Services/AOAI connection. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)
| `network-secured-agent.bicep`  | Deploy a network secured agent setup that uses User Managed Identity authentication on the Agent Connections. | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fnetwork-secured-agent%2Fazuredeploy.json)


**Manually Deploy Templates**

<details>
<summary><b>Option 1</b>: Use basic agent setup.</summary>

1. To authenticate to your Azure subscription from the Azure CLI, use the following command:

   > [!NOTE]
   > Be sure to run these commands with the subscription that has been allowlisted for the private preview.

   ```console
   az login
   ```

2. Create a resource group:

   ```console
   az group create --name {my_resource_group} --location eastus
   ```

   Make sure you have the role **Azure AI Developer** on the resource group you just created.
3. Download the `basic-agent-keys.bicep` file, `basic-agent-identity.bicep` file, and the `modules-basic` folder to your project directory. Your directory should look like this

    ```console
    /my-project
        - basic-agent-keys.bicep
        - basic-agent-identity.bicep
        - basic-agent.parameters.json
        /modules-basic
            - basic-ai-hub-keys.bicep
            - basic-ai-project-keys.bicep
            - basic-ai-hub-identity.bicep
            - basic-ai-project-identity.bicep
            - basic-dependent-resources.bicep
    ```
4. Before deploying resources, decide which configuration file to use:
    - `basic-agent-keys.bicep`: Uses API key authentication on the AI Services/AOAI connection.
    - `basic-agent-identity.bicep`: Uses Managed Identity authentication on the AI Services/AOAI connection.

5. Using the resource group you created in the previous step and one of the template files (either basic-agent-keys.bicep or basic-agent-identity.bicep), run one of the following commands:

    - To use default resource names, run:

    ```console
    az deployment group create --resource-group {my_resource_group} --template-file {my-template-file.bicep}
    ```

    - To specify custom names for the hub, project, storage account, and/or Azure AI service resources (Note: a randomly generated suffix will be added to prevent accidental duplication), run:

    ```console
    az deployment group create --resource-group {my_resource_group} --template-file {my-template-file.bicep} --parameters aiHubName='your-hub-name' aiProjectName='your-project-name' storageName='your-storage-name' aiServicesName='your-ai-services-name'
    ```

    - To customize additional parameters, including the OpenAI model deployment, download and edit the `basic-agent.parameters.json` file, then run:

    ```console
    az deployment group create --resource-group {my_resource_group} --template-file  {my-template-file.bicep} --parameters @basic-agent.parameters.json
    ```

Resources for the hub, project, storage account, and AI Services will be created for you. The AI Services account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region. A Microsoft-managed key vault will be used by default. To deploy a Llama model see [here](https://github.com/Azure/azure-ai-agents/blob/main/samples/llama-3.md).

</details>


<details>
    <summary><b>Option 2</b>: Use standard agent setup.</summary>

1. To authenticate to your Azure subscription from the Azure CLI, use the following command:

   > [!NOTE]
   > Be sure to run these commands with the subscription that has been allowlisted for the private preview.

   ```console
   az login
   ```

2. Create a resource group:

   ```console
   az group create --name {my_resource_group} --location eastus
   ```

   Make sure you have the role **Azure AI Developer** on the resource group you just created. 
3. Download the `standard-agent.bicep` file, the `standard-agent.parameters.json` file, and the `modules-standard` folder to your project directory. Your directory should look like this

    ```console
    /my-project
        - standard-agent.bicep
        - standard-agent.parameters.json 
        /modules-standard
            - standard-ai-hub.bicep
            - standard-ai-project.bicep
            - standard-dependent-resources.bicep
    ```
4. Using the resource group you created in the previous step, run one of the following commands:

    - To use default resource names, run:

    ```console
    az deployment group create --resource-group {my_resource_group} --template-file standard-agent.bicep
    ```

    - To customize additional parameters, including the OpenAI model deployment, hub name, etc, download and edit the `standard-agent.parameters.json` file, then run:

    ```console
        az deployment group create --resource-group {my_resource_group} --template-file standard-agent.bicep --parameters @standard-agent.parameters.json
    ```

    Resources for the hub, project, storage account, key vault, AI Services, and Azure AI Search will be created for you. The AI Services, AI Search, and Azure Blob Storage account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region. To deploy a Llama model see [here](https://github.com/Azure/azure-ai-agents/blob/main/samples/llama-3.md).


</details>


## Configure and run your first agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

Use the following code to create an agent and send a message to it. This agent will have the code interpreter tool to enable your agent to perform advanced data analysis in a sandboxed environment.

## Python SDK

### Setup

1. Run the following commands to install the python packages. 

    ```console
    pip install azure-ai-projects
    pip install azure-identity
    ```


### Create an Agent

Use the following code to create and run an agent. To run this code, you will need to create a connection string using information from your project. This string is in the format:

`<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>`

`HostName` can be found by navigating to your `discovery_url` and removing the leading `https://` and trailing `/discovery`. To find your `discovery_url`, run this CLI command:

`az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url`

For example, your connection string may look something like:

`eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name`

Set this connection string as an environment variable named `PROJECT_CONNECTION_STRING`.

> [!TIP]
> Want to use the OpenAI SDK? You can find [examples of using the Azure AI Agent service with the OpenAI SDK](./samples/use-openai.md) in the samples folder of this repo.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.identity import DefaultAzureCredential
from typing import Any
from pathlib import Path

# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Create an instance of the CodeInterpreterTool
    code_interpreter = CodeInterpreterTool()

    # The CodeInterpreterTool needs to be included in creation of the agent
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
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
        project_client.agents.save_file(file_id=file_path_annotation.file_path.file_id, file_name=Path(file_path_annotation.text).name)

    # Delete the agent once done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```

## C#

```Cs
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#nullable disable

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Core.TestFramework;
using NUnit.Framework;

namespace Azure.AI.Projects.Tests;

public partial class Sample_Agent_Basics : SamplesBase<AIProjectsTestEnvironment>
{
    [Test]
    public async Task BasicExample()
    {
        var connectionString = Environment.GetEnvironmentVariable("AZURE_AI_CONNECTION_STRING");

        AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());
        #endregion

        // Step 1: Create an agent
        #region Snippet:OverviewCreateAgent
        Response<Agent> agentResponse = await client.CreateAgentAsync(
            model: "gpt-4o",
            name: "Math Tutor",
            instructions: "You are a personal math tutor. Write and run code to answer math questions.",
            tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() });
        Agent agent = agentResponse.Value;
        #endregion

        // Intermission: agent should now be listed

        Response<PageableList<Agent>> agentListResponse = await client.GetAgentsAsync();

        //// Step 2: Create a thread
        #region Snippet:OverviewCreateThread
        Response<AgentThread> threadResponse = await client.CreateThreadAsync();
        AgentThread thread = threadResponse.Value;
        #endregion

        // Step 3: Add a message to a thread
        #region Snippet:OverviewCreateMessage
        Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
            thread.Id,
            MessageRole.User,
            "I need to solve the equation `3x + 11 = 14`. Can you help me?");
        ThreadMessage message = messageResponse.Value;
        #endregion

        // Intermission: message is now correlated with thread
        // Intermission: listing messages will retrieve the message just added

        Response<PageableList<ThreadMessage>> messagesListResponse = await client.GetMessagesAsync(thread.Id);
        Assert.That(messagesListResponse.Value.Data[0].Id == message.Id);

        // Step 4: Run the agent
        #region Snippet:OverviewCreateRun
        Response<ThreadRun> runResponse = await client.CreateRunAsync(
            thread.Id,
            agent.Id,
            additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");
        ThreadRun run = runResponse.Value;
        #endregion

        #region Snippet:OverviewWaitForRun
        do
        {
            await Task.Delay(TimeSpan.FromMilliseconds(500));
            runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
        }
        while (runResponse.Value.Status == RunStatus.Queued
            || runResponse.Value.Status == RunStatus.InProgress);
        #endregion

        #region Snippet:OverviewListUpdatedMessages
        Response<PageableList<ThreadMessage>> afterRunMessagesResponse
            = await client.GetMessagesAsync(thread.Id);
        IReadOnlyList<ThreadMessage> messages = afterRunMessagesResponse.Value.Data;

        // Note: messages iterate from newest to oldest, with the messages[0] being the most recent
        foreach (ThreadMessage threadMessage in messages)
        {
            Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
            foreach (MessageContent contentItem in threadMessage.ContentItems)
            {
                if (contentItem is MessageTextContent textItem)
                {
                    Console.Write(textItem.Text);
                }
                else if (contentItem is MessageImageFileContent imageFileItem)
                {
                    Console.Write($"<image from ID: {imageFileItem.FileId}");
                }
                Console.WriteLine();
            }
        }
        #endregion
    }
}

```
