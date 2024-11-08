# <imports_and_config>
import os
import pandas as pd
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.ai.evaluation import evaluate, GroundednessEvaluator, F1ScoreEvaluator, RelevanceEvaluator
from azure.identity import DefaultAzureCredential

from chat_with_products import chat_with_products

# load environment variables from the .env file at the root of this repo
from dotenv import load_dotenv
load_dotenv()

# create a project client using environment variables loaded from the .env file
project = AIProjectClient.from_connection_string(
    conn_str=os.environ['AIPROJECT_CONNECTION_STRING'],
    credential=DefaultAzureCredential()
)

connection = project.connections.get_default(
    connection_type=ConnectionType.AZURE_OPEN_AI,
    with_credentials=True)

# TODO: provide a better way to get this from project client
evaluator_model = {
    "azure_endpoint": connection.endpoint_url,
    "azure_deployment": os.environ["EVALUATION_MODEL"],
    "api_version": "2024-06-01",
    "api_key": connection.key,
}

groundedness = GroundednessEvaluator(evaluator_model)
# </imports_and_config>

# <evaluate_wrapper>
# create a wrapper function that implements the evaluation interface for query & response evaluation
def evaluate_chat_with_products(query):
    response = chat_with_products(messages=[{"role": "user", "content": query}])
    return {
        "response": response["message"].content,
        "context": response["context"]["grounding_data"]
    }
# </evaluate_wrapper>

# <run_evaluation>
# Evaluate must be called inside of a __name__ == "__main__" block
if __name__ == "__main__":
    from config import ASSET_PATH

    # workaround for multiprocessing issue on linux
    from pprint import pprint
    import multiprocessing
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass  # Start method has already been set, so we can ignore this error

    result = evaluate(
        data=os.path.join(ASSET_PATH, "chat_eval_data.jsonl"),
        target=evaluate_chat_with_products,
        evaluation_name="evaluate_chat_with_products",
        evaluators={
            "groundedness": groundedness,
        },
        evaluator_config={
            "default": {
                "query": {"${data.query}"},
                "response": {"${target.response}"},
                "context": {"${target.context}"},
            }
        },
        output_path="./myevalresults.json"
    )

    tabular_result = pd.DataFrame(result.get("rows"))

    pprint("-----Summarized Metrics-----")
    pprint(result["metrics"])
    pprint("-----Tabular Result-----")
    pprint(tabular_result)
    pprint(f"View evaluation results in AI Studio: {result['studio_url']}")
# </run_evaluation>