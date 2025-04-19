from typing import Any, List

# Azure AI Projects

from azure.ai.projects.models import BingGroundingTool, FilePurpose, FileSearchTool, FunctionTool, ToolSet

# Your custom Python functions (for "fetch_weather","fetch_stock_price","send_email","fetch_datetime", etc.)
from enterprise_functions import enterprise_fns

# Function titles for tool bubbles
function_titles = {
    "fetch_weather": "☁️ fetching weather",
    "fetch_datetime": "🕒 fetching datetime",
    "fetch_stock_price": "📈 fetching financial info",
    "send_email": "✉️ sending mail",
    "file_search": "📄 searching docs",
    "bing_grounding": "🔍 searching bing",
}


def set_up_enterprise_toolset(project_client):
    import os
    from dotenv import load_dotenv

    load_dotenv()

    try:
        bing_connection = project_client.connections.get(connection_name=os.environ["BING_CONNECTION_NAME"])
        conn_id = bing_connection.id
        bing_tool = BingGroundingTool(connection_id=conn_id)
        print("bing > connected")
    except Exception as e:
        bing_tool = None
        print("bing failed > no connection found or permission issue")
        print(e)

    FOLDER_NAME = "enterprise-data"
    VECTOR_STORE_NAME = "hr-policy-vector-store"
    all_vector_stores = project_client.agents.list_vector_stores().data
    existing_vector_store = next((store for store in all_vector_stores if store.name == VECTOR_STORE_NAME), None)

    vector_store_id = None
    if existing_vector_store:
        vector_store_id = existing_vector_store.id
        print(f"reusing vector store > {existing_vector_store.name} (id: {existing_vector_store.id})")
    else:
        # If you have local docs to upload
        import os

        if os.path.isdir(FOLDER_NAME):
            file_ids = []
            for file_name in os.listdir(FOLDER_NAME):
                file_path = os.path.join(FOLDER_NAME, file_name)
                if os.path.isfile(file_path):
                    print(f"uploading > {file_name}")
                    uploaded_file = project_client.agents.upload_file_and_poll(
                        file_path=file_path, purpose=FilePurpose.AGENTS
                    )
                    file_ids.append(uploaded_file.id)

            if file_ids:
                print(f"creating vector store > from {len(file_ids)} files.")
                vector_store = project_client.agents.create_vector_store_and_poll(
                    file_ids=file_ids, name=VECTOR_STORE_NAME
                )
                vector_store_id = vector_store.id
                print(f"created > {vector_store.name} (id: {vector_store_id})")

    file_search_tool = None
    if vector_store_id:
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store_id])

    # Combine All Tools into a ToolSet
    # This step creates a custom ToolSet that includes all the tools configured earlier. It also adds a LoggingToolSet subclass to log the inputs and outputs of function calls.

    class LoggingToolSet(ToolSet):
        def execute_tool_calls(self, tool_calls: List[Any]) -> List[dict]:
            """
            Execute the upstream calls, printing only two lines per function:
            1) The function name + its input arguments
            2) The function name + its output result
            """

            # For each function call, print the input arguments
            for c in tool_calls:
                if hasattr(c, "function") and c.function:
                    fn_name = c.function.name
                    fn_args = c.function.arguments
                    print(f"{fn_name} inputs > {fn_args} (id:{c.id})")

            # Execute the tool calls (superclass logic)
            raw_outputs = super().execute_tool_calls(tool_calls)

            # Print the output of each function call
            for item in raw_outputs:
                print(f"output > {item['output']}")

            return raw_outputs

    custom_functions = FunctionTool(enterprise_fns)

    toolset = LoggingToolSet()
    if bing_tool:
        toolset.add(bing_tool)
    if file_search_tool:
        toolset.add(file_search_tool)
    toolset.add(custom_functions)

    for tool in toolset._tools:
        tool_name = tool.__class__.__name__
        print(f"tool > {tool_name}")
        for definition in tool.definitions:
            if hasattr(definition, "function"):
                fn = definition.function
                print(f"{fn.name} > {fn.description}")
            else:
                pass

    # (Optional) Direct Azure AI Search Integration
    # If the default File Search Tool is available, we add it and skip the Azure AI Search integration.
    if any(tool.__class__.__name__ == "FileSearchTool" for tool in toolset._tools) or True:
        print("file_search tool exists > skipping ai_search tool add")
    else:
        try:
            # Get the connection ID for your Azure AI Search resource
            connections = project_client.connections.list()
            conn_id = next(c.id for c in connections if c.name == os.environ.get("AZURE_SEARCH_CONNECTION_NAME"))

            # Initialize Azure AI Search tool for direct index access
            from azure.ai.projects.models import AzureAISearchTool

            search_tool = AzureAISearchTool(
                index_connection_id=conn_id, index_name=os.environ.get("AZURE_SEARCH_INDEX_NAME")
            )

            # Add the Azure AI Search tool to our toolset
            toolset.add(search_tool)
            print("azure ai search > connected directly to index")

            # Verify the tool was added by iterating through the toolset
            for tool in toolset._tools:
                tool_name = tool.__class__.__name__
                print(f"tool > {tool_name}")
                for definition in tool.definitions:
                    if hasattr(definition, "function"):
                        fn = definition.function
                        print(f"{fn.name} > {fn.description}")
                    else:
                        pass

        except Exception as e:
            print(f"azure ai search > skipped (no connection configured): {e!s}")
    return toolset
