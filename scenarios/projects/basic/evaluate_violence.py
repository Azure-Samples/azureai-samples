# ruff: noqa: E402

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# <evaluate_violence>
from azure.ai.evaluation import ViolenceEvaluator
from azure.identity import DefaultAzureCredential

# Initializing Violence Evaluator with project information
violence_eval = ViolenceEvaluator(azure_ai_project=project.scope, credential=DefaultAzureCredential())

# Running Violence Evaluator on single input row
violence_score = violence_eval(query="what's the capital of france", response="Paris")
print(violence_score)
# </evaluate_violence>
