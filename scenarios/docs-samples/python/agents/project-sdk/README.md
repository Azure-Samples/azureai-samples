# Azure Agent Samples – Python Project SDK

This README demonstrates how to use Azure AI Projects to build intelligent agents powered by custom tools. These tools enable agents to perform practical real-world tasks such as running code, searching documents, invoking APIs, and automating workflows.

## Prerequisites

Before running the samples, ensure the following environment variables are set:

- `PROJECT_CONNECTION_STRING`: Connection string for your Azure AI Foundry project.
- `MODEL_DEPLOYMENT_NAME`: Name of the deployed model to use (e.g., `gpt-4o-mini`).

## Tools

---

### Code Interpreter

*Sample:* [`code-interpreter.py`](./code-interpreter.py)

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

*Sample:* [`file-search.py`](./file-search.py)

File Search augments the agent with knowledge from external documents, such as proprietary product information or user-provided files.

#### Workflow:

1. **Upload Files**: Upload files to the Azure AI project.
2. **Create a Vector Store**: Index the uploaded files into a vector store for semantic search.
3. **Query the Agent**: Use the agent to perform searches across the indexed files.

**Note:** Vector stores are temporary and have a default expiration policy of seven days.

**Note:** Ensure all files are fully indexed before querying (status != `in_progress`).

---

### Function Calling

*Samples:*  
- [`python-function-calling.py`](./python-function-calling.py)  
- [`python-function-calling-toolset.py`](./python-function-calling-toolset.py)  
- [`python-function-calling-streaming.py`](./python-function-calling-streaming.py)

This tool allows agents to call your custom Python functions dynamically.

#### Example functions:
- `fetch_current_datetime()`  
- `fetch_weather()`  
- `send_email(recipient, subject, body)`

#### Execution Pattern:
```python
functions = FunctionTool(functions=user_functions)
agent = project_client.agents.create_agent(
    tools=functions.definitions,
    ...
)

run = project_client.agents.create_run(thread_id=thread.id, agent_id=agent.id)
# Monitor and execute required function calls
```

---

### Logic App Integration

*Sample:* [`sample_agents_logic_apps.py`](./sample_agents_logic_apps.py)

Use Logic Apps to extend your agent with enterprise-grade workflows. This is ideal for automating tasks such as notifications, scheduling, CRM updates, and more.

#### Setup Code:

**Initialize Tool:**
```python
logic_app_tool = AzureLogicAppTool(subscription_id, resource_group)
logic_app_tool.register_logic_app(logic_app_name, trigger_name)
```

**Wrap Logic App Trigger as a Function:**
```python
send_email_func = create_send_email_function(logic_app_tool, logic_app_name)
```

**Tool Binding:**
```python
functions = FunctionTool(functions={fetch_current_datetime, send_email_func})
toolset = ToolSet()
toolset.add(functions)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="SendEmailAgent",
    instructions="You are a specialized agent for sending emails.",
    toolset=toolset,
)
```

---

### OpenAPI Connections

*Sample:* [`sample_agents_openapi_connection_auth.py`](./sample_agents_openapi_connection_auth.py)

This tool connects agents to 3rd-party REST APIs using OpenAPI schemas. Great for accessing real-time data from services like TripAdvisor, Yelp, Stripe, etc.

#### Key Features:
- Parses `.json` OpenAPI specs
- Authenticates with API keys or OAuth
- Generates callable API functions for agents

---

### Bing Integration

*Sample:* [`bing-integration.py`](./bing-integration.py)

Integrate Bing Search to enable agents to fetch real-time web search results. This is useful for retrieving the latest news, web content, or answering general knowledge queries.

#### Setup Code:

**Initialize Bing Tool:**
```python
bing_tool = BingSearchTool(api_key=os.environ["BING_API_KEY"])
```

**Agent Setup:**
```python
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="BingSearchAgent",
    instructions="You are an agent that fetches real-time web search results.",
    tools=bing_tool.definitions,
)
```

**Example Query:**
> "Find the latest news about AI advancements."

---

### Azure Functions

*Sample:* [`azure_functions.py`](./azure_functions.py)

Azure Functions allow agents to interact with serverless functions triggered by Azure Storage Queues. This is ideal for scenarios requiring asynchronous processing or integration with other Azure services.

#### Setup Code:

**Initialize Azure Function Tool:**
```python
azure_function_tool = AzureFunctionTool(
    name="foo",
    description="Get answers from the foo bot.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The question to ask."},
            "outputqueueuri": {"type": "string", "description": "The full output queue uri."},
        },
    },
    input_queue=AzureFunctionStorageQueue(
        queue_name="azure-function-foo-input",
        storage_service_endpoint=os.environ["STORAGE_SERVICE_ENDPONT"],
    ),
    output_queue=AzureFunctionStorageQueue(
        queue_name="azure-function-tool-output",
        storage_service_endpoint=os.environ["STORAGE_SERVICE_ENDPONT"],
    ),
)
```

**Agent Setup:**
```python
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="azure-function-agent-foo",
    instructions="You are a helpful support agent. Use the provided function any time the prompt contains the string 'What would foo say?'.",
    tools=azure_function_tool.definitions,
)
```

**Example Query:**
> "What is the most prevalent element in the universe? What would foo say?"

---
