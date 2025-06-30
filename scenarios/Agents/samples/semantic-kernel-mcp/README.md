# Using MCP Servers with Azure AI Foundry Agent service and Semantic Kernel

Semantic Kernel has been deeply integrated with the agent service and allows you to easily add additional tools to your Agent. 
The Model Context Protocol (MCP) is a protocol for exposing tools and other context to models. Semantic Kernel has built-in support for all types of MCP Servers and after reading the definition, it exposes the tools and prompts of the MCP server to the agent that consumes them.

## Setup

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and optionally [docker](https://www.docker.com/products/docker-desktop/)
1. Ensure you have your Azure AI Foundry Hub and Agent setup done, see [here](../README.md), and add the project connection string and model deployment name to a .env file (or copy the .env.example), with the following names:
    - AZURE_AI_AGENT_PROJECT_CONNECTION_STRING
    - AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME
1. If you want to run the Stdio Server sample: Create a Personal Access Token for Github that has read access to the repositories that you want to interact with, see [the documentation](https://github.com/modelcontextprotocol/servers/tree/main/src/github) on how to create one.
1. If you want to run the Sse Server sample: add the URL of the MCP server to the .env file, under the `MCP_SERVER_URL` variable.
1. Navigate into this folder and call `uv run agent_with_stdio_server.py` or `uv run agent_with_sse_server.py` this will automatically create a venv with the required packages installed.

> You can also run the samples with python, just make sure to check the required dependencies in the pyproject.toml file.
