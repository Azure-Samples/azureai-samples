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

# Set "./assets" as the path where assets are stored, resolving the absolute path:
ASSET_PATH = os.path.join(pathlib.Path(__file__).parent.resolve(), "assets")

# Configure an root app logger that prints info level logs to stdout
root_logger = logging.getLogger("app")
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# Returns a module-specific logger, inheriting from the root app logger
def get_logger(module_name):
    logger = logging.getLogger(f"app.{module_name}")
    return logger

# Enable instrumentation and logging of telemetry to the project
def enable_telemetry(log_to_project : bool = False):
    AIInferenceInstrumentor().instrument()

    # enable logging message contents
    os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true"

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
