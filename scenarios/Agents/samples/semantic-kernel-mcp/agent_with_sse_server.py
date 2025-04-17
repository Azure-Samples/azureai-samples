# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from dotenv import load_dotenv

from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.connectors.mcp import MCPSsePlugin

"""
The following sample demonstrates how to create a AzureAIAgent that
uses a SSE based MCP server to add context to the Agent.

It uses the Azure AI Foundry Agent service to create a agent, so make sure to 
set the required environment variables for the Azure AI Foundry service:
- AZURE_AI_AGENT_PROJECT_CONNECTION_STRING
- AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME
"""

load_dotenv()


async def main() -> None:
    """Main function that creates the plugin, the agent and starts the conversation loop."""
    async with (
        # 1. Login to Azure and create a Azure AI Project Client
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds) as client,
        # 2. Create the MCP plugin
        MCPSsePlugin(
            name="mcp",
            description="MCP Plugin",
            url=os.getenv("MCP_SERVER_URL"),
        ) as plugin,
    ):
        # 3. Create the agent, with the MCP plugin and the thread
        agent = AzureAIAgent(
            client=client,
            definition=await client.agents.create_agent(
                model=AzureAIAgentSettings.create().model_deployment_name,
                name="GithubAgent",
                instructions="You are a microsoft/semantic-kernel Issue Triage Agent. "
                "You look at all issues that have the tag: 'triage' and 'python'."
                "When you find one that is untriaged, you will suggest a new assignee "
                "based on the issue description, look at recent closed PR's for issues in the same area. "
                "You will also suggest additional context if needed, like related issues or a bug fix. ",
            ),
            plugins=[plugin],  # add the sample plugin to the agent
        )
        thread: AzureAIAgentThread | None = None
        # 4. Print instructions and set the initial user input
        print("Starting Azure AI Agent with MCP Plugin sample...")
        print("Once the first prompt is answered, you can further ask questions, use `exit` to exit.")
        user_input = input("# User: ")
        try:
            while user_input.lower() != "exit":
                # 5. Invoke the agent for a response
                response = await agent.get_response(messages=user_input, thread=thread)
                print(f"# {response.name}: {response} ")
                thread = response.thread
                # 6. Get a new user input
                user_input = input("# User: ")
        finally:
            # 7. Cleanup: Clear the thread
            await thread.delete() if thread else None
            await client.agents.delete_agent(agent.definition.id)


if __name__ == "__main__":
    asyncio.run(main())
