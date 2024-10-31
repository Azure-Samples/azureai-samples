# Use OpenAPI 3.0 Specified Tools 

The Custom Tools feature allows developers to describe custom tools in the Agent API using an [OpenAPI schema](https://www.openapis.org/), enabling the model to intelligently call these functions based on user input. You can use any API spec that is written according to the OpenAPI 3.0 schema.   

## Setup 

First you need a tool defined using the OpenAPI Schema, for example:  

```yml
openapi: 3.0.1  
info:  
  title: Weather Service API  
  description: This is a sample API for retrieving weather information.  
  version: 1.0.0  
servers:  
  - url: https://api.example.com/weather  
    description: Main API Server  
paths:  
  /current:  
    get:  
      summary: Get current weather  
      operationId: getCurrentWeather 
... 
```

## Example 

> [!NOTE]
> You can find [C# code below](#c).

```python
import os, time  
from azure.ai.projects import AIProjectClient  
from azure.identity import DefaultAzureCredential  
from azure.ai.projects.models import openapi, SubmitToolOutputsAction, RequiredFunctionToolCall  

# Create an Azure AI Client from a connection string, copied from your AI Studio project.  
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"  
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables  

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

with project_client:
    # Create an agent and run user's request with function calls
    agent = project_client.agents.create_agent(
        model="gpt-4-1106-preview",
        name="my-agent",
        instructions="You are a helpful agent",
        tools=[{
            "type": "openapi",
            "openapi": {
                "name": "mytool",
                "description": "My tool",
                "spec": {
                    "openapi": "3.0.0",
                    <your schema definition goes here>
                }
            },
            "auth": {
                "type": "anonymous | managed_identity | connection"
            }
        }]
    )
    print(f"Created agent, ID: {agent.id}")

    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Hello, send an email with the datetime and weather information in New York?",
    )
    print(f"Created message, ID: {message.id}")

    run = project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Created run, ID: {run.id}")

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            if not tool_calls:
                print("No tool calls provided - cancelling run")
                project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                break

            tool_outputs = []
            for tool_call in tool_calls:
                if isinstance(tool_call, RequiredFunctionToolCall):
                    try:
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                        })
                    except Exception as e:
                        print(f"Error executing tool_call {tool_call.id}: {e}")

            print(f"Tool outputs: {tool_outputs}")
            if tool_outputs:
                project_client.agents.submit_tool_outputs_to_run(
                    thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                )

        print(f"Current run status: {run.status}")

    print(f"Run completed with status: {run.status}")

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
using System.Threading.Tasks;
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Projects.Models;

class Program
{
    static async Task Main(string[] args)
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
        var projectClient = new AIProjectClient(connectionString, credential);

        // Create an agent and run user's request with function calls
        var agent = await projectClient.Agents.CreateAgentAsync(new CreateAgentOptions
        {
            Model = "gpt-4-1106-preview",
            Name = "my-agent",
            Instructions = "You are a helpful agent",
            Tools = new[]
            {
                new Tool
                {
                    Type = "openapi",
                    OpenApi = new OpenApiTool
                    {
                        Name = "mytool",
                        Description = "My tool",
                        Spec = new OpenApiSpec
                        {
                            OpenApi = "3.0.0",
                            // <your schema definition goes here>
                        }
                    }
                }
            }
        });

        // Use the agent as needed
        // ...
    }
}
```

 

Authentication can be either anonymous (no authentication) or “managed_identity” 

"auth": { "type": "managed_identity", "security_scheme": { "audience": "https://cognitiveservices.azure.com/" }} 

 or “connection” 

"auth": { "type": "connection", "security_scheme": { "connection_id": "1234-56789" }} 

anonymous is not authentication, managed_identity is authenticating with various Azure Services using RBAC, connection is using 3rd party APIs with API keys and Custom Keys Connections in azure AI studio.  

Note: Connection authentication requires an enterprise setup. 