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