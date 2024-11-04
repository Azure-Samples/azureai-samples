import os 

from azure.ai.projects.models import bing_grounding, ToolSet  
from azure.ai.projects import AIProjectClient 
from azure.identity import DefaultAzureCredential 

from azure.ai.ml.entities import WorkspaceConnection 
from azure.ai.ml.entities import UsernamePasswordConfiguration, ApiKeyConfiguration 

 
# Create an Azure AI Client from a connection string, copied from your AI Studio project. 
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>" 
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables 
 
project_client = AIProjectClient.from_connection_string( 
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"] 
) 

 

# Customer needs to create a connection to the Grounding with Bing Search resource 

connection_name = "bing_grounding_connection" 

  

target = “GROUNDING_WITH_BING_SEARCH_API” 

wps_connection = WorkspaceConnection( 
     name=connection_name, 
     type="custom", 
     target=target, 
     credentials=ApiKeyConfiguration(key="API_KEY"),     
 ) 
 ml_client.connections.create_or_update(workspace_connection=wps_connection) 

with project_client: 
 
    # Create Grounding with Bing Search tool with resources 
    bing_grounding_tool = bing_grounding(connection_id=[connection id of Grounding with Bing Search resource]) 
 
    # Create agent with SharePoint tool and process agent run 
    agent = project_client.agents.create_agent( 
        model="gpt-4-1106-preview", 
        name="my-agent", 
        instructions="Hello, you are helpful agent and can search information from uploaded files", 
        tools=bing_grounding_tool.definitions, 
        tool_resources= bing_grounding_tool.resources, 
    ) 
    print(f"Created agent, agent ID: {agent.id}") 
 
    # Create thread for communication 
    thread = project_client.agents.create_thread() 
    print(f"Created thread, ID: {thread.id}") 
 
    # Create message to thread 
    message = project_client.agents.create_message( 
        thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?" 
    ) 
    print(f"Created message, ID: {message.id}") 
 
    # Create and process agent run in thread with tools 
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id) 
    print(f"Run finished with status: {run.status}") 
 
    if run.status == "failed": 
        # Check if you got "Rate limit is exceeded.", then you want to get more quota 
        print(f"Run failed: {run.last_error}")  

    if run.status == “complete”: 

print(f"Run complete: {run.id}") 
	 

# Delete the agent when done 
project_client.agents.delete_agent(agent.id) 
print("Deleted agent") 

# Fetch and log all messages 
messages = project_client.agents.list_messages(thread_id=thread.id) 
print(f"Messages: {messages}") 