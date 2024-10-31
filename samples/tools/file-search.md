# File Search

File Search augments the Agent with knowledge from outside its model, such as proprietary product information or documents provided by your users. OpenAI automatically parses and chunks your documents, creates and stores the embeddings, and use both vector and keyword search to retrieve relevant content to answer user queries. 

## Setup 

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the in_progress state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling. 

## Example 

> [!NOTE]
> You can find [C# code below](#c).

### Python 

```python
import os 
from azure.ai.projects import AIProjectClient 
from azure.ai.projects.models._patch import FileSearchTool 
from azure.identity import DefaultAzureCredential 
 
 
# Create an Azure AI Client from a connection string, copied from your AI Studio project. 
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>" 
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables 
 
project_client = AIProjectClient.from_connection_string( 
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"] 
) 

 
with project_client: 
 
    openai_file = project_client.agents.upload_file_and_poll(file_path="product_info_1.md", purpose="assistants") 
    print(f"Uploaded file, file ID: {openai_file.id}") 
 
    openai_vectorstore = project_client.agents.create_vector_store_and_poll(file_ids=[openai_file.id], name="my_vectorstore") 
    print(f"Created vector store, vector store ID: {openai_vectorstore.id}") 
 
    # Create file search tool with resources 
    file_search = FileSearchTool(vector_store_ids=[openai_vectorstore.id]) 
 
    # Create agent with file search tool and process the agent run 
    agent = project_client.agents.create_agent( 
        model="gpt-4-1106-preview", 
        name="my-agent", 
        instructions="Hello, you are helpful agent and can search information from uploaded files", 
        tools=file_search.definitions, 
        tool_resources=file_search.resources, 
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
 
    # Delete the file when done 
    project_client.agents.delete_vector_store(openai_vectorstore.id) 
    print("Deleted vector store") 
 
    # Delete the agent when done 
    project_client.agents.delete_agent(agent.id) 
    print("Deleted agent") 
 
    # Fetch and log all messages 
    messages = project_client.agents.list_messages(thread_id=thread.id) 
    print(f"Messages: {messages}") 
```
 

### C# 

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Azure.Identity;
using NUnit.Framework;

namespace Azure.AI.Projects.Tests
{
    public partial class Sample_Agent_FileSearch
    {
        [Test]
        public async Task FilesSearchExample()
        {
            var connectionString = Environment.GetEnvironmentVariable("AZURE_AI_CONNECTION_STRING");
            AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());

            #region Snippet:UploadAgentFilesToUse
            // Upload a file and wait for it to be processed
            File.WriteAllText(
                path: "sample_file_for_upload.txt",
                contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
            Response<AgentFile> uploadAgentFileResponse = await client.UploadFileAsync(
                filePath: "sample_file_for_upload.txt",
                purpose: AgentFilePurpose.Agents);

            AgentFile uploadedAgentFile = uploadAgentFileResponse.Value;
            #endregion

            #region Snippet:CreateVectorStore
            // Create a vector store with the file and wait for it to be processed.
            // If you do not specify a vector store, create_message will create a vector store with a default expiration policy of seven days after they were last active
            VectorStore vectorStore = await client.CreateVectorStoreAsync(
                fileIds: new List<string> { uploadedAgentFile.Id },
                name: "my_vector_store");
            #endregion

            #region Snippet:CreateAgentWithFiles
            FileSearchToolResource fileSearchToolResource = new FileSearchToolResource();
            fileSearchToolResource.VectorStoreIds.Add(vectorStore.Id);

            // Create an agent with toolResources and process the agent run
            Response<Agent> agentResponse = await client.CreateAgentAsync(
                model: "gpt-4-1106-preview",
                name: "SDK Test Agent - Retrieval",
                instructions: "You are a helpful agent that can help fetch data from files you know about.",
                tools: new List<ToolDefinition> { new FileSearchToolDefinition() },
                toolResources: new ToolResources() { FileSearch = fileSearchToolResource });
            Agent agent = agentResponse.Value;
            #endregion

            // Create thread for communication
            Response<AgentThread> threadResponse = await client.CreateThreadAsync();
            AgentThread thread = threadResponse.Value;

            // Create message to thread
            Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
                thread.Id,
                MessageRole.User,
                "Can you give me the documented codes for 'banana' and 'orange'?");
            ThreadMessage message = messageResponse.Value;

            // Run the agent
            Response<ThreadRun> runResponse = await client.CreateRunAsync(thread, agent);

            do
            {
                await Task.Delay(TimeSpan.FromMilliseconds(500));
                runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
            }
            while (runResponse.Value.Status == RunStatus.Queued
                || runResponse.Value.Status == RunStatus.InProgress);

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