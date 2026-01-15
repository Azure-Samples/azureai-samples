# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
import time
from pprint import pprint

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)


def run_evaluator(
    evaluator_name: str,
    evaluation_contents: list[SourceFileContentContent],
    data_source_config: dict,
    initialization_parameters: dict[str, str],
    data_mapping: dict[str, str],
) -> list:#list of type
    """
    Run an evaluator on the provided evaluation contents.
    
    Args:
        evaluator_name: Name of the evaluator (e.g., "tool-success")
        evaluation_contents: List of test cases to evaluate
        data_source_config: Configuration for the data source schema
        initialization_parameters: Parameters for initializing the evaluator
        data_mapping: Mapping of data fields to evaluator inputs
        
    Returns:
        List of evaluation output items with results
    """
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    
    with DefaultAzureCredential() as credential:
        with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
            client = project_client.get_openai_client()

            testing_criteria = [
                {
                    "type": "azure_ai_evaluator",
                    "name": f"{evaluator_name}",
                    "evaluator_name": f"builtin.{evaluator_name}",
                    "initialization_parameters": initialization_parameters,
                    "data_mapping": data_mapping,
                }
            ]

            eval_object = client.evals.create(
                name=f"Test {evaluator_name} Evaluator with inline data",
                data_source_config=data_source_config,
                testing_criteria=testing_criteria,
            )

            eval_run_object = client.evals.runs.create(
                eval_id=eval_object.id,
                name="inline_data_run",
                metadata={"team": "eval-exp", "scenario": "inline-data-v1"},
                data_source=CreateEvalJSONLRunDataSourceParam(
                    type="jsonl",
                    source=SourceFileContent(type="file_content", content=evaluation_contents)
                ),
            )

            print(f"Eval Run created with ID: {eval_run_object.id}")
            print("Waiting for eval run to complete...")

            while True:
                run = client.evals.runs.retrieve(run_id=eval_run_object.id, eval_id=eval_object.id)
                if run.status == "completed" or run.status == "failed":
                    output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id))
                    print(f"✓ Eval Run Status: {run.status}")
                    print(f"📊 Eval Run Report URL: {run.report_url}")
                    
                    return output_items
                    
                time.sleep(5)
