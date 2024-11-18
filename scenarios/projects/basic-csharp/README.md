
## Projects

Install the projects package and identity package:
```
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.Identity
```

Add using statements:
```cs
using Azure.Identity;
using Azure.AI.Projects;
```

## Azure OpenAI Service

Install Azure OpenAI:
```
dotnet add package Azure.AI.OpenAI --prerelease
```

```cs
using OpenAI.Chat;
using Azure.AI.OpenAI;
```

## Azure AI model inference service

Install the inferencing package:
```
dotnet add package Azure.AI.Inference --prerelease
```

Add using statements:
```cs
using Azure.AI.Inference;
```

## Azure AI Search Service

Install Azure AI Search package:
```
dotnet add package Azure.Search.Documents
```

Add using statements:
```cs
using Azure.Search.Documents;
using Azure.Search.Documents.Models;
```

## Tracing

Tracing is not yet integrated into the projects package, see [here](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Inference/samples/Sample8_ChatCompletionsWithOpenTelemetry.md) for instructions on how to instrument and log traces from the Azure AI Inferencing package.

## RAG Sample

See [here](https://azure.github.io/ai-app-templates/repo/azure-samples/azure-search-openai-demo-csharp/) for a RAG sample that uses Azure OpenAI and Azure AI Search.

## Prompt Templating

Prompt templating is not yet integrated into the C# inferencing package. See [this blog post](https://devblogs.microsoft.com/dotnet/add-ai-to-your-dotnet-apps-easily-with-prompty/) for how to use Semantic Kernel with Prompty.

## Evaluation

An Azure AI evaluation package is not yet available for C#. See [here](https://github.com/Azure-Samples/contoso-chat-csharp-prompty/blob/main/src/ContosoChatAPI/ContosoChat.Evaluation.Tests/Evalutate.cs) for a sample on how to use Prompty and Semantic Kernel for evaluation.
