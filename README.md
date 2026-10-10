
# Azure AI Samples

[![license: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

Welcome to the Azure AI Samples repository!

This repository acts as the top-level directory for official Azure AI sample code and examples. It includes notebooks and sample code that contain end-to-end samples as well as smaller code snippets for common developer tasks.

This repository is entirely open source, guidance on how to contribute and links to additional repositories are provided below.

Use the samples in this repository to try out Azure AI scenarios on your local machine!

## Samples in this Repository

All samples are organized under the [`scenarios/`](./scenarios) directory. Each scenario folder contains its own README, notebooks, and supporting files.

| Scenario | Description |
|---|---|
| [Agents](./scenarios/Agents/samples) | Quickstart and tool-specific samples for the **Azure AI Agent Service** — covers Bing Search grounding, Code Interpreter, File Search, Function Calling, investment-advisor and sales-analyst end-to-end notebooks, Semantic Kernel + MCP integration, and agent tracing. |
| [Assistants](./scenarios/Assistants) | **Azure OpenAI Assistants API** samples including bot-in-a-box templates, BFSI bot, function calling with Bing Search, and a multi-agent pattern. |
| [GPT-4V](./scenarios/GPT-4V) | **GPT-4 Vision** samples covering basic inference, OCR, grounding, face detection, multi-image, RAG with images, and video analysis. |
| [agent-tracing](./scenarios/agent-tracing) | **OpenTelemetry-based tracing** for agents built with LangChain, LangGraph, and the OpenAI Agents SDK, with support for local OTLP backends and Azure Monitor. |
| [evaluate](./scenarios/evaluate) | **AI evaluation** samples using the `azure-ai-evaluation` SDK — simulators, safety/quality evaluators, custom evaluators, NLP metrics, and Azure OpenAI graders. |
| [fine-tuning](./scenarios/fine-tuning) | **Fine-tuning** samples for Azure OpenAI models, including function-calling fine-tunes. |
| [langchain](./scenarios/langchain) | **LangChain** integration with Azure AI Foundry — chat models, embeddings, and tracing. |
| [llama-index](./scenarios/llama-index) | **LlamaIndex** integration with Azure AI Foundry — RAG query routing and tracing. |
| [model-catalog](./scenarios/model-catalog) | Getting-started samples for models in the **Azure AI model catalog**. |
| [projects](./scenarios/projects) | **Azure AI Projects SDK** basics — inference, chat, evaluation, search, tracing, and Prompty usage. |
| [rag](./scenarios/rag) | **Custom RAG application** built code-first with Azure AI Search and Azure AI Foundry, including evaluation and simulation. |
| [resource-creation](./scenarios/resource-creation) | Notebooks for programmatically creating **Azure AI hubs, projects, and connections**. |

## Supplementary Documentation

### Other Sample Repositories

#### Azure AI Agent Service

* **[Azure/azure-sdk-for-python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents)** - Repo containing Python SDK samples for the Azure AI Agent Service.
* **[Azure/azure-sdk-for-net](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/tests/Samples/Agent)** - Repo containing .NET SDK samples for the Azure AI Agent Service.
* **[Azure-Samples/azureai-travel-agent-python](https://github.com/Azure-Samples/azureai-travel-agent-python/tree/main)** - Sample showing how to build a travel agent using the Azure AI Agent Service in Python.
* **[Azure-Samples/azure-ai-projects-file-search](https://github.com/Azure-Samples/azure-ai-projects-file-search)** - A simple Python Quart app that streams responses from Azure AI Agents to an HTML/JS frontend using Server-Sent Events (SSEs).

#### Azure AI Foundry

* **[Azure/aistudio-copilot-sample]** - Quickstart repo for building an enterprise chat copilot in Azure AI Studio.
* **[Azure-Samples/contoso-chat](https://github.com/Azure-Samples/contoso-chat)** - End-to-end solution sample for a custom RAG-based retail copilot built code-first with Prompty & Azure AI Studio.
* **[Azure-Samples/contoso-creative-writer](https://github.com/Azure-Samples/contoso-creative-writer)** - End-to-end solution sample for a custom multi-agent creative writer solution built code-first with Prompty & Azure AI Studio.

#### Azure AI Search

* **[Azure-Samples/azure-search-openai-demo]** - Repo containing end to end samples for running the Retrieval
  Augmented Generation pattern across data using Python.
* **[Azure-Samples/azure-search-openai-javascript]** - Repo containing end to end samples for running the Retrieval
  Augmented Generation pattern across data using JavaScript.
* **[Azure-Samples/azure-search-openai-demo-csharp]** - Repo containing end to end samples for running the Retrieval
  Augmented Generation pattern across data using .NET.
* **[Azure-Samples/azure-search-openai-demo-java]** - Repo containing end to end samples for running the Retrieval
  Augmented Generation pattern across data using Java.
* **[Azure-Samples/langchainjs-quickstart-demo]** - Sample showing how to quickly develop generative AI apps using LangChain.js, starting with Ollama and local models and transition to Azure for production.
* **[Azure-Samples/azure-openai-rag-workshop]** - Repo contains both a sample and a step-by-step workshop on how to build a custom chatbot with Retrieval
  Augmented Generation using JavaScript.

#### Azure AI Assistant
* **[Azure-Samples/azure-ai-assistant-tool]** - Repo containing the Azure AI Assistant Tool and Python middleware libraries for quick experimentation, testing, and debugging of Azure OpenAI assistants in your local environment.

#### Copilot

* **[microsoft/chat-copilot]** - Sample showing how to build LLM chat copilot.

#### OpenAI

* **[openai/openai-cookbook]** - Example code for common tasks within OpenAI.
* **[Azure-Samples/serverless-chat-langchainjs](https://github.com/Azure-Samples/serverless-chat-langchainjs)** - Sample implementing a serverless ChatGPT with Retrieval-Augmented-Generation using LangChain.js, that can run locally with Ollama and Mistral 7B.

#### Phi
* **[Phi-3 Cookbook](https://aka.ms/phi-3cookbook)** - Examples and code for common tasks using the Phi Family of Small Language Models.

## Contributing

We welcome contributions and suggestions! Please see the [contributing guidelines] for details.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Please see the [code of conduct](.github/CODE_OF_CONDUCT.md) for details.

## Getting Help

### Issues

If you find a bug in the source code or a mistake in the documentation, feel free to [submit bug report][new issue page]
. Or you could submit a pull request with a fix.

### Feature Requests

If there's an sample that you'd like to see added, feel free to file a [Feature Request][new issue page].

If you'd like to implement it yourself, please refer to our [contributing guidelines].

[Azure/aistudio-copilot-sample]: https://github.com/Azure/aistudio-copilot-sample
[Azure-Samples/azure-search-openai-demo]: https://github.com/Azure-Samples/azure-search-openai-demo
[Azure-Samples/azure-search-openai-javascript]: https://github.com/Azure-Samples/azure-search-openai-javascript
[Azure-Samples/azure-search-openai-demo-csharp]: https://github.com/Azure-Samples/azure-search-openai-demo-csharp
[Azure-Samples/azure-search-openai-demo-java]: https://github.com/Azure-Samples/azure-search-openai-demo-java
[Azure-Samples/langchainjs-quickstart-demo]: https://github.com/Azure-Samples/langchainjs-quickstart-demo
[Azure-Samples/azure-openai-rag-workshop]: https://github.com/Azure-Samples/azure-openai-rag-workshop/tree/base
[Azure-Samples/azure-ai-assistant-tool]: https://github.com/Azure-Samples/azureai-assistant-tool
[contributing guidelines]: ./CONTRIBUTING.md
[microsoft/chat-copilot]: https://github.com/microsoft/chat-copilot
[new issue page]: https://github.com/Azure-Samples/azureai-samples/issues/new/choose
[openai/openai-cookbook]: https://github.com/openai/openai-cookbook/tree/main/examples
[Azure-Samples/serverless-chat-langchainjs]: https://github.com/Azure-Samples/serverless-chat-langchainjs