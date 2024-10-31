# Function Calling 

Azure AI Agents Service supports function calling, which allows you to describe the structure of functions to an Agent and then return the functions that need to be called along with their arguments.

## Example

> [!NOTE]
> You can find [C# code below](#c).

```python
import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, SubmitToolOutputsAction, RequiredFunctionToolCall
from user_functions import user_functions


# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

# Initialize function tool with user functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent and run user's request with function calls
    agent = project_client.agents.create_agent(
        model="gpt-4-1106-preview",
        name="my-agent",
        instructions="You are a helpful agent",
        tools=functions.definitions,
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

    run = project_client.agents.create_run(thread_id=thread.id, agent_id=agent.id)
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
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Azure.Identity;
using NUnit.Framework;

namespace Azure.AI.Projects.Tests
{
    public partial class Sample_Agent_Functions
    {
        [Test]
        public async Task FunctionCallingExample()
        {
            var connectionString = Environment.GetEnvironmentVariable("AZURE_AI_CONNECTION_STRING");
            AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());

            #region Snippet:FunctionsDefineFunctionTools
            // Example of a function that defines no parameters
            string GetUserFavoriteCity() => "Seattle, WA";
            FunctionToolDefinition getUserFavoriteCityTool = new("getUserFavoriteCity", "Gets the user's favorite city.");

            // Example of a function with a single required parameter
            string GetCityNickname(string location) => location switch
            {
                "Seattle, WA" => "The Emerald City",
                _ => throw new NotImplementedException(),
            };
            FunctionToolDefinition getCityNicknameTool = new(
                name: "getCityNickname",
                description: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
                parameters: BinaryData.FromObjectAsJson(
                    new
                    {
                        Type = "object",
                        Properties = new
                        {
                            Location = new
                            {
                                Type = "string",
                                Description = "The city and state, e.g. San Francisco, CA",
                            },
                        },
                        Required = new[] { "location" },
                    },
                    new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }));

            // Example of a function with one required and one optional, enum parameter
            string GetWeatherAtLocation(string location, string temperatureUnit = "f") => location switch
            {
                "Seattle, WA" => temperatureUnit == "f" ? "70f" : "21c",
                _ => throw new NotImplementedException()
            };
            FunctionToolDefinition getCurrentWeatherAtLocationTool = new(
                name: "getCurrentWeatherAtLocation",
                description: "Gets the current weather at a provided location.",
                parameters: BinaryData.FromObjectAsJson(
                    new
                    {
                        Type = "object",
                        Properties = new
                        {
                            Location = new
                            {
                                Type = "string",
                                Description = "The city and state, e.g. San Francisco, CA",
                            },
                            Unit = new
                            {
                                Type = "string",
                                Enum = new[] { "c", "f" },
                            },
                        },
                        Required = new[] { "location" },
                    },
                    new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }));
            #endregion

            #region Snippet:FunctionsHandleFunctionCalls
            ToolOutput GetResolvedToolOutput(RequiredToolCall toolCall)
            {
                if (toolCall is RequiredFunctionToolCall functionToolCall)
                {
                    if (functionToolCall.Name == getUserFavoriteCityTool.Name)
                    {
                        return new ToolOutput(toolCall, GetUserFavoriteCity());
                    }
                    using JsonDocument argumentsJson = JsonDocument.Parse(functionToolCall.Arguments);
                    if (functionToolCall.Name == getCityNicknameTool.Name)
                    {
                        string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
                        return new ToolOutput(toolCall, GetCityNickname(locationArgument));
                    }
                    if (functionToolCall.Name == getCurrentWeatherAtLocationTool.Name)
                    {
                        string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
                        if (argumentsJson.RootElement.TryGetProperty("unit", out JsonElement unitElement))
                        {
                            string unitArgument = unitElement.GetString();
                            return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument, unitArgument));
                        }
                        return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument));
                    }
                }
                return null;
            }
            #endregion

            #region Snippet:FunctionsCreateAgentWithFunctionTools
            // note: parallel function calling is only supported with newer models like gpt-4-1106-preview
            Response<Agent> agentResponse = await client.CreateAgentAsync(
                model: "gpt-4-1106-preview",
                name: "SDK Test Agent - Functions",
                instructions: "You are a weather bot. Use the provided functions to help answer questions. "
                    + "Customize your responses to the user's preferences as much as possible and use friendly "
                    + "nicknames for cities whenever possible.",
                tools: new List<ToolDefinition> { getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool }
            );
            Agent agent = agentResponse.Value;
            #endregion

            Response<AgentThread> threadResponse = await client.CreateThreadAsync();
            AgentThread thread = threadResponse.Value;

            Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
                thread.Id,
                MessageRole.User,
                "What's the weather like in my favorite city?");
            ThreadMessage message = messageResponse.Value;

            Response<ThreadRun> runResponse = await client.CreateRunAsync(thread, agent);

            #region Snippet:FunctionsHandlePollingWithRequiredAction
            do
            {
                await Task.Delay(TimeSpan.FromMilliseconds(500));
                runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);

                if (runResponse.Value.Status == RunStatus.RequiresAction
                    && runResponse.Value.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
                {
                    List<ToolOutput> toolOutputs = new();
                    foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
                    {
                        toolOutputs.Add(GetResolvedToolOutput(toolCall));
                    }
                    runResponse = await client.SubmitToolOutputsToRunAsync(runResponse.Value, toolOutputs);
                }
            }
            while (runResponse.Value.Status == RunStatus.Queued
                || runResponse.Value.Status == RunStatus.InProgress);
            #endregion

            Response<PageableList<ThreadMessage>> afterRunMessagesResponse = await client.GetMessagesAsync(thread.Id);
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
                        Console.Write($"<image from ID: {imageFileItem.FileId}>");
                    }
                    Console.WriteLine();
                }
            }
        }
    }
}
```

# Samples

Get the latest stock price using function calling with Yfinance ([shown in Personal Finance Assistant](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/Assistants/api-in-a-box/personal_finance/assistant-personal_finance.ipynb))
