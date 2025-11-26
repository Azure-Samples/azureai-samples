import os

import dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from azure.identity import DefaultAzureCredential

dotenv.load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project_client.get_openai_client()

tools = [
    MCPTool(
        # This is just a placeholder. Connection details are in
        # the project connection referenced by `project_connection_id`.
        server_url="https://localhost",
        server_label="python_tool",
        require_approval="never",
        allowed_tools=[
            "launchShell",
            "runPythonCodeInRemoteEnvironment",
        ],
        project_connection_id=os.environ["AZURE_AI_CONNECTION_ID"],
    ),
]

EXAMPLE_DATA_FILE_URL = "https://raw.githubusercontent.com/Azure-Samples/azureai-samples/refs/heads/main/scenarios/Agents/data/nifty_500_quarterly_results.csv"

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="""\
You are a helpful agent that can use a Python code interpreter to assist users. Use the `python_tool` MCP
server to perform any calculations or numerical analyses. ALWAYS call the `launchShell` tool first before
calling the `runPythonCodeInRemoteEnvironment` tool. If you need to provide any non-text data to the user,
always print a data URI with the contents. NEVER provide a path to a file in the remote environment to the user.
""",
            temperature=0,
            tools=tools,
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Use the agent to analyze a CSV file and produce a histogram
    response = openai_client.responses.create(
        input=f"Please analyze the CSV file at {EXAMPLE_DATA_FILE_URL}. Could you please create bar chart in the TRANSPORTATION sector for the operating profit and provide a file to me?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"[Response {response.id}]: {response.output_text}")

    # Clean up resources by deleting the agent version
    # This prevents accumulation of unused agent versions in your project
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
