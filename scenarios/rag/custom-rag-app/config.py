import os
import sys
import pathlib
import logging

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.tracing import AIInferenceInstrumentor

# load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

LOGGING_HANDLER = logging.StreamHandler(stream=sys.stdout)
LOGGING_LEVEL = logging.INFO
ASSET_PATH = os.path.join(pathlib.Path(__file__).parent.resolve(), "assets")

def enable_telemetry(log_to_project : bool = False):
    AIInferenceInstrumentor().instrument()

    if log_to_project:
        from azure.monitor.opentelemetry import configure_azure_monitor

        project = AIProjectClient.from_connection_string(
            conn_str=os.environ['AIPROJECT_CONNECTION_STRING'],
            credential=DefaultAzureCredential()
        )
        application_insights_connection_string = project.telemetry.get_connection_string()
        if not application_insights_connection_string:
            "No application insights connection string found. Telemetry will not be logged to project."
            return
        
        configure_azure_monitor(connection_string=application_insights_connection_string)
        print("Enabled telemetry logging to project, view traces at:")
        print(f"https://int.ai.azure.com/project-monitoring?wsid=/subscriptions/{project.scope['subscription_id']}/resourceGroups/{project.scope['resource_group_name']}/providers/Microsoft.MachineLearningServices/workspaces/{project.scope['project_name']}")
