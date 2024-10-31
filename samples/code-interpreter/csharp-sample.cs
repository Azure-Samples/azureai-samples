using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

class Program
{
    private static readonly string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");
    private static readonly string apiVersion = "2024-05-01-preview";
    private static readonly string azureEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");

    static async Task Main(string[] args)
    {
        var client = new HttpClient();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);

        // Upload a file with an "assistants" purpose
        var fileContent = new StreamContent(File.OpenRead("speech.py"));
        var fileRequest = new MultipartFormDataContent();
        fileRequest.Add(fileContent, "file", "speech.py");
        fileRequest.Add(new StringContent("assistants"), "purpose");

        var fileResponse = await client.PostAsync($"{azureEndpoint}/v1/files?api-version={apiVersion}", fileRequest);
        var fileResponseBody = await fileResponse.Content.ReadAsStringAsync();
        var fileId = JObject.Parse(fileResponseBody)["id"].ToString();

        // Create an assistant using the file ID
        var assistantRequest = new
        {
            instructions = "You are an AI assistant that can write code to help answer math questions.",
            model = "gpt-4-1106-preview",
            tools = new[] { new { type = "code_interpreter" } },
            tool_resources = new { code_interpreter = new { file_ids = new[] { fileId } } }
        };

        var assistantResponse = await client.PostAsJsonAsync($"{azureEndpoint}/v1/assistants?api-version={apiVersion}", assistantRequest);
        var assistantResponseBody = await assistantResponse.Content.ReadAsStringAsync();
        var assistantId = JObject.Parse(assistantResponseBody)["id"].ToString();

        // Create a thread with the assistant
        var threadRequest = new
        {
            messages = new[]
            {
                new
                {
                    role = "user",
                    content = "I need to solve the equation `3x + 11 = 14`. Can you help me?",
                    file_ids = new[] { fileId }
                }
            }
        };

        var threadResponse = await client.PostAsJsonAsync($"{azureEndpoint}/v1/threads?api-version={apiVersion}", threadRequest);
        var threadResponseBody = await threadResponse.Content.ReadAsStringAsync();
        Console.WriteLine(threadResponseBody);
    }
}