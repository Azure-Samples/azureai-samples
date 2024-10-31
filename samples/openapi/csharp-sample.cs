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