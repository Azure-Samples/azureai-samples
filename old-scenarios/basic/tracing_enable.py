# ruff: noqa: E402

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# <enable_tracing>
# Enable instrumentation of AI packages (inference, agents, openai, langchain)
from azure.monitor.opentelemetry import configure_azure_monitor

# Enable OpenTelemetry instrumentation of the Inference SDK, add other OpenTelemetry instrumenters as needed
project.telemetry.enable(destination=None)

# Construct a URL for the project's tracing page
project_url = f"https://ai.azure.com/tracing?wsid=/subscriptions/{project.scope['subscription_id']}/resourceGroups/{project.scope['resource_group_name']}/providers/Microsoft.MachineLearningServices/workspaces/{project.scope['project_name']}"

# Log telemetry to the project's application insights resource
application_insights_connection_string = project.telemetry.get_connection_string()
if application_insights_connection_string:
    print(f"Enabled logging telemetry to project, view traces at:\n{project_url}")
    configure_azure_monitor(connection_string=application_insights_connection_string)
else:
    print(f"Application Insights is not configured for this project. Configure Application Insights at:\n{project_url}")
# </enable_tracing>
