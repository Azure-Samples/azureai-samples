# Azure Agent Samples – Python Project SDK

This README demonstrates how to use Azure AI Projects to build intelligent agents powered by custom tools. These tools enable agents to perform practical real-world tasks such as running code, searching documents, invoking APIs, and automating workflows.

## Prerequisites

Before running the samples, ensure the following environment variables are set:

- `PROJECT_CONNECTION_STRING`: Connection string for your Azure AI Foundry project.
- `MODEL_DEPLOYMENT_NAME`: Name of the deployed model to use (e.g., `gpt-4o-mini`).

## Tools

---

### Code Interpreter

*Sample:* [`code_interpreter.py`](./code_interpreter.py)

The Code Interpreter tool allows the agent to write and execute Python code in a sandboxed environment. It enables the agent to:

- Analyze structured data (e.g., CSVs)
- Generate visualizations
- Process numerical or textual information
- Output annotated results and downloadable files

#### Key Code Snippets

**File Upload:**
```python
file = project_client.agents.upload_file_and_poll(
    file_path="nifty_500_quarterly_results.csv", 
    purpose=FilePurpose.AGENTS
)
```

**Code Interpreter Setup:**
```python
code_interpreter = CodeInterpreterTool(file_ids=[file.id])
```

**Agent Setup:**
```python
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-assistant",
    instructions="You are a helpful assistant",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

---

### File Search

*Sample:* [`file_search.py`](./file_search.py)

File Search augments the agent with knowledge from external documents, such as proprietary product information or user-provided files.

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the in_progress state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling.

#### File Sources
- Uploading local files
- Use project data assets (i.e., existing files in the Azure Storage Account connected to the project)

#### Basic Agent Setup <br> 
The File Search tool has the same functionality as AOAI Assistants. Microsoft managed search and storage resources are used. 
- Uploaded files get stored in Microsoft managed storage
- A vector store is created using a Microsoft managed search resource

#### Standard Agent Setup 
The File Search tool uses the Azure AI Search and Azure Blob Storage resources you connected during agent setup.  
- Uploaded files get stored in your connected Azure Blob Storage account
- Vector stores get created using your connected Azure AI Seach resource

For both Agent setups, OpenAI handles the entire ingestion process, including automatically parsing and chunking documents, generating and storing embeddings, and utilizing both vector and keyword searches to retrieve relevant content for user queries.

There is no difference in the code between the two setups; the only variation is in where your files and created vector stores are stored.

---

### Azure AI Search
*Sample:* [`azure_ai_search_tool.py`](./azure_ai_search_tool.py)
This tool allows you to use an existing Azure AI Search index with your Agent. 

Azure AI Search indexes must meet the following requirements
- The index must contain at least one searchable & retrievable text field (type Edm.String)
- The index must contain at least one searchable vector field (type Collection(Edm.Single))
- The index is assumed to be configured properly

Required parameters:
- index_connection_id
- index_name
  
Additional optional parameters:
- query_type: The search type for your index
- top_k: How many documents to retrieve from search and present to the model
- filter: OData filter string configured by the client. [Learn more about text query filters](https://learn.microsoft.com/en-us/azure/search/search-filters)

Search Types
You can specify the search type for your index by choosing one of the following
- Simple
- Semantic
- Vector
- Hybrid (Vector + Keyword)
- Hybrid (Vector + Keyword + Semantic)

---

### Function Calling

*Samples:*  
- [`python_function_calling.py`](./python_function_calling.py)  
- [`python_function_calling-toolset.py`](./python_function-calling_toolset.py)  
- [`python_function_calling-streaming.py`](./python_function_calling_streaming.py)

This tool allows agents to call your custom Python functions dynamically.

#### Example functions:
- `fetch_current_datetime()`  
- `fetch_weather()`  
- `send_email(recipient, subject, body)`

---

### Logic Apps Integration

*Sample:* [`sample_agents_logic_apps.py`](./sample_agents_logic_apps.py)

Use Logic Apps to extend your agent with enterprise-grade workflows. This is ideal for automating tasks such as notifications, scheduling, CRM updates, and more.

---

### OpenAPI Connections

*Sample:* [`sample_agents_openapi_connection_auth.py`](./sample_agents_openapi_connection_auth.py)

This tool connects agents to 3rd-party REST APIs using OpenAPI schemas. Great for accessing real-time data from services like TripAdvisor, Yelp, Stripe, etc.

#### Key Features:
- Parses `.json` OpenAPI specs
- Authenticates with API keys or OAuth
- Generates callable API functions for agents

---

### Grounding with Bing Search

*Sample:* [`bing_grounding.py`](./bing_grounding.py)

Grounding with Bing Search allows your Azure AI Agents to incorporate real-time public web data when generating responses. To start with, you need to create a Grounding with Bing Search resource, then connect this resource to your Azure AI Agents. When a user sends a query, Azure AI Agents will decide if Grounding with Bing Search should be leveraged or not. If so, it will leverage Bing to search over public web data and return relevant chunks. Lastly, Azure AI Agents will use returned chunks to generate a response.

Citations show links to websites used to generate response, but don’t show links to the bing query used for the search. Developers and end users don’t have access to raw content returned from Grounding with Bing Search.

You can ask questions such as "what is the weather in Seattle?" "what is the recent update in ratail industry in the US?" that require real-time public data.

---

### Azure Functions

*Sample:* [`azure_functions.py`](./azure_functions.py)

Azure Functions allow agents to interact with serverless functions triggered by Azure Storage Queues. This is ideal for scenarios requiring asynchronous processing or integration with other Azure services.

---
