# Grounding with Bing Search 

Grounding with Bing Search allows your Azure Agents to incorporate real-time public web data when generating responses. To start with, you need to create a Grounding with Bing Search resource, then connect this resource to your Azure Agents. When a user sends a query, Azure Agents will decide if Grounding with Bing Search should be leveraged or not. If so, it will leverage Bing to search over public web data and return relevant chunks. Lastly, Azure Agents will use returned chunks to generate a response.  

Citations show links to websites used to generate response, but don’t show links to the bing query used for the search. Developers and end users don’t have access to raw content returned from Bing 

Please note that developers and end users don’t have access to raw chunks returned by Grounding with Bing Search. Grounding with Bing Search is a free service during private preview. 	 

## Setup  

Create a Bing Search resource. If you don’t have one, you can use the Azure CLI or Azure portal to create one: 

```console
az cognitiveservices account create \ 

  --name bing-grounding-resource \ 
  --resource-group <resource-group-name> \ 
  --kind Bing.Grounding \ 
  --sku G1 \ 
  --location Global \ 
  --yes 
```

## Example 

> [!NOTE]
> You can find [C# code below](#c).

### Python 

```python
import os 

from azure.ai.projects.models import bing_grounding, ToolSet  
from azure.ai.projects import AIProjectClient 
from azure.identity import DefaultAzureCredential 

from azure.ai.ml.entities import WorkspaceConnection 
from azure.ai.ml.entities import UsernamePasswordConfiguration, ApiKeyConfiguration 

 
# Create an Azure AI Client from a connection string, copied from your AI Studio project. 
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>" 
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables 
 
project_client = AIProjectClient.from_connection_string( 
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"] 
) 

 

# Customer needs to create a connection to the Grounding with Bing Search resource 

connection_name = "bing_grounding_connection" 

  

target = “GROUNDING_WITH_BING_SEARCH_API” 

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
 
    # Create agent with SharePoint tool and process agent run 
    agent = project_client.agents.create_agent( 
        model="gpt-4-1106-preview", 
        name="my-agent", 
        instructions="Hello, you are helpful agent and can search information from uploaded files", 
        tools=bing_grounding_tool.definitions, 
        tool_resources= bing_grounding_tool.resources, 
    ) 
    print(f"Created agent, agent ID: {agent.id}") 
 
    # Create thread for communication 
    thread = project_client.agents.create_thread() 
    print(f"Created thread, ID: {thread.id}") 
 
    # Create message to thread 
    message = project_client.agents.create_message( 
        thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?" 
    ) 
    print(f"Created message, ID: {message.id}") 
 
    # Create and process agent run in thread with tools 
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id) 
    print(f"Run finished with status: {run.status}") 
 
    if run.status == "failed": 
        # Check if you got "Rate limit is exceeded.", then you want to get more quota 
        print(f"Run failed: {run.last_error}")  

    if run.status == “complete”: 

print(f"Run complete: {run.id}") 
	 
 
    # Delete the agent when done 
    project_client.agents.delete_agent(agent.id) 
    print("Deleted agent") 
 
    # Fetch and log all messages 
    messages = project_client.agents.list_messages(thread_id=thread.id) 
    print(f"Messages: {messages}") 
```

## C# 

```csharp
using System;
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Projects.Models;
using Azure.AI.ML.Entities;

class Program
{
    static void Main(string[] args)
    {
        // Ensure the environment variable is set
        string connectionString = Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
        if (string.IsNullOrEmpty(connectionString))
        {
            Console.WriteLine("Please set the PROJECT_CONNECTION_STRING environment variable.");
            return;
        }

        // Create an Azure AI Client from a connection string
        var credential = new DefaultAzureCredential();
        var projectClient = AIProjectClient.FromConnectionString(credential, connectionString);

        // Create a connection to the Grounding with Bing Search resource
        string connectionName = "bing_grounding_connection";
        string target = "GROUNDING_WITH_BING_SEARCH_API";

        var wpsConnection = new WorkspaceConnection
        {
            Name = connectionName,
            Type = "custom",
            Target = target
        };

        // Additional code to use the projectClient and wpsConnection can be added here
    }
}
```

## Samples

* [Assistant function calling with Bing Search](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants/function_calling)