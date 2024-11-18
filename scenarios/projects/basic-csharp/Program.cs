using Azure.AI.Projects;
using Azure.Identity;

// Azure AI model inference imports
using Azure.AI.Inference;

// Azure OpenAI imports
using OpenAI.Chat;
using Azure.AI.OpenAI;

// Azure AI Search imports
using Azure.Search.Documents;
using Azure.Search.Documents.Models;

using NUnit.Framework;

namespace Azure.AI.Samples
{
    public partial class Program
    {
        public async static Task Main(string[] args)
        {
            if (args.Length < 1) {
                return;
            }
            
            String sample = args[0];
            Console.WriteLine(sample);

            if (sample == "inference") {
                Inference();
            } else if (sample == "basic") {
                await AgentsBasic();
            } else if (sample == "azureopenai") {
                AzureOpenAI();
            } else if (sample == "basic-streaming") {
                await AgentsBasicStreaming();
            } 
        }

        public static void GetProject()
        {
            // <snippet_get_project>
            var connectionString = "<your_connection_string>";
            var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());
            // </snippet_get_project>

        }

        public static void AzureOpenAI()
        {
            var connectionString = Environment.GetEnvironmentVariable("AIPROJECT_CONNECTION_STRING");
            var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());

            // <azure_openai>
            var connections = projectClient.GetConnectionsClient();
            var connection = connections.GetDefaultConnection(ConnectionType.AzureAIServices, withCredential: true);

            AzureOpenAIClient azureOpenAIClient = new(
                new Uri(connection.Properties.Target),
                new AzureKeyCredential(connection.Properties.Credentials.Key));

            // This must match the custom deployment name you chose for your model
            ChatClient chatClient = azureOpenAIClient.GetChatClient("gpt-4o-mini");

            ChatCompletion completion = chatClient.CompleteChat(
                [
                    new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
                    new UserChatMessage("Does Azure OpenAI support customer managed keys?"),
                    new AssistantChatMessage("Yes, customer managed keys are supported by Azure OpenAI"),
                    new UserChatMessage("Do other Azure AI services support this too?")
                ]);

            Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
            // </azure_openai>
        }

        public static void Inference()
        {
            // <snippet_inference>
            var connectionString = Environment.GetEnvironmentVariable("AIPROJECT_CONNECTION_STRING");
            var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());

            ChatCompletionsClient chatClient = projectClient.GetChatCompletionsClient();

            var requestOptions = new ChatCompletionsOptions()
            {
                Messages =
                    {
                        new ChatRequestSystemMessage("You are a helpful assistant."),
                        new ChatRequestUserMessage("How many feet are in a mile?"),
                    },
                Model = "gpt-4o-mini"
            };

            Response<ChatCompletions> response = chatClient.Complete(requestOptions);
            Console.WriteLine(response.Value.Content);
            // </snippet_inference>
        }


        public static void AzureAISearch()
        {
            var connectionString = Environment.GetEnvironmentVariable("AIPROJECT_CONNECTION_STRING");
            var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());

            // <azure_aisearch>
            var connections = projectClient.GetConnectionsClient();
            var connection = connections.GetDefaultConnection(ConnectionType.AzureAISearch, withCredential: true);

            SearchClient searchClient = new SearchClient(
                new Uri(connection.Properties.Target),
                new AzureKeyCredential(connection.Properties.Credentials.Key));
            // </azure_aisearch>
        }
        
        // Prompty: https://devblogs.microsoft.com/dotnet/add-ai-to-your-dotnet-apps-easily-with-prompty/
        // Tracing: https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md
        // RAG sample: https://azure.github.io/ai-app-templates/repo/azure-samples/azure-search-openai-demo-csharp/
        // Evaluation sample: https://github.com/Azure-Samples/contoso-chat-csharp-prompty/blob/main/src/ContosoChatAPI/ContosoChat.Evaluation.Tests/Evalutate.cs

        public static async Task AgentsBasic()
        {
            Console.WriteLine($"-------- Azure AI Basic Sample --------");

            var connectionString = Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
            AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());

            // Step 1: Create an agent
            Response<Agent> agentResponse = await client.CreateAgentAsync(
                model: "gpt-4-1106-preview",
                name: "Math Tutor",
                instructions: "You are a personal math tutor. Write and run code to answer math questions.",
                tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() });
            Agent agent = agentResponse.Value;

            // Intermission: agent should now be listed

            Response<PageableList<Agent>> agentListResponse = await client.GetAgentsAsync();

            //// Step 2: Create a thread
            Response<AgentThread> threadResponse = await client.CreateThreadAsync();
            AgentThread thread = threadResponse.Value;

            // Step 3: Add a message to a thread
            Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
                thread.Id,
                MessageRole.User,
                "I need to solve the equation `3x + 11 = 14`. Can you help me?");
            ThreadMessage message = messageResponse.Value;

            // Intermission: message is now correlated with thread
            // Intermission: listing messages will retrieve the message just added

            Response<PageableList<ThreadMessage>> messagesListResponse = await client.GetMessagesAsync(thread.Id);
            Assert.That(messagesListResponse.Value.Data[0].Id == message.Id);

            // Step 4: Run the agent
            Response<ThreadRun> runResponse = await client.CreateRunAsync(
                thread.Id,
                agent.Id,
                additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");
            ThreadRun run = runResponse.Value;

            do
            {
                await Task.Delay(TimeSpan.FromMilliseconds(500));
                runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
            }
            while (runResponse.Value.Status == RunStatus.Queued
                || runResponse.Value.Status == RunStatus.InProgress);

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
        }

        public static async Task AgentsBasicStreaming()
        {
            Console.WriteLine($"-------- Azure AI Streaming Sample--------");

            var connectionString = Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
            AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());

            Response<Agent> agentResponse = await client.CreateAgentAsync(
                model: "gpt-4-1106-preview",
                name: "My Friendly Test Assistant",
                instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
                tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() });
            Agent agent = agentResponse.Value;

            Response<AgentThread> threadResponse = await client.CreateThreadAsync();
            AgentThread thread = threadResponse.Value;

            Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
                thread.Id,
                MessageRole.User,
                "Hi, Assistant! Draw a graph for a line with a slope of 4 and y-intercept of 9.");
            ThreadMessage message = messageResponse.Value;

            await foreach (var streamingUpdate in client.CreateRunStreamingAsync(thread.Id, agent.Id))
            {
                Console.WriteLine(streamingUpdate.UpdateKind);
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
