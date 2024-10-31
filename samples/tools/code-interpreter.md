# Code interpreter 

Code Interpreter allows the Agent to write and run Python code in a sandboxed execution environment. With Code Interpreter enabled, your Agent can run code iteratively to solve more challenging code, math, and data analysis problems.

## Supported file types

|File format|MIME Type|
|---|---|
|.c| text/x-c |
|.cpp|text/x-c++ |
|.csv|application/csv|
|.docx|application/vnd.openxmlformats-officedocument.wordprocessingml.document|
|.html|text/html|
|.java|text/x-java|
|.json|application/json|
|.md|text/markdown|
|.pdf|application/pdf|
|.php|text/x-php|
|.pptx|application/vnd.openxmlformats-officedocument.presentationml.presentation|
|.py|text/x-python|
|.py|text/x-script.python|
|.rb|text/x-ruby|
|.tex|text/x-tex|
|.txt|text/plain|
|.css|text/css|
|.jpeg|image/jpeg|
|.jpg|image/jpeg|
|.js|text/javascript|
|.gif|image/gif|
|.png|image/png|
|.tar|application/x-tar|
|.ts|application/typescript|
|.xlsx|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet|
|.xml|application/xml or "text/xml"|
|.zip|application/zip|

## Example 

Use the following examples to use Code interpreter with file attachment.

> [!NOTE]
> You can find [C# code below](#c).

### Python 

```python
from openai import AzureOpenAI 
     
client = AzureOpenAI( 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),   
    api_version="2024-05-01-preview", 
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
    ) 
 
# Upload a file with an "assistants" purpose 
file = client.files.create( 
  file=open("speech.py", "rb"), 
  purpose='assistants' 
) 
 
# Create an assistant using the file ID 
assistant = client.beta.assistants.create( 
  instructions="You are an AI assistant that can write code to help answer math questions.", 
  model="gpt-4-1106-preview", 
  tools=[{"type": "code_interpreter"}], 
  tool_resources={"code interpreter":{"file_ids":[file.id]}} 
) 

client = AzureOpenAI( 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),   
    api_version="2024-05-01-preview", 
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
    ) 
 
thread = client.beta.threads.create( 
  messages=[ 
    { 
      "role": "user", 
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?", 
      "file_ids": ["file.id"] # file id will look like: "assistant-R9uhPxvRKGH3m0x5zBOhMjd2"  
    } 
  ] 
) 
``` 

## C# 

```csharp
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
```

# Samples

* [Math tutor](https://github.com/openai/openai-cookbook/blob/main/examples/data/oai_docs/tool-code-interpreter.txt)