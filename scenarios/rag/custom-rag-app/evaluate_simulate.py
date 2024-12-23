# ruff: noqa
# File is WIP

from chat_with_products import chat_with_products
import os

from azure.ai.evaluation.simulator import Simulator
from azure.ai.evaluation import evaluate, CoherenceEvaluator, FluencyEvaluator
from typing import Any, Dict, List, Optional
import asyncio
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

connection = project.connections.get_default(connection_type=ConnectionType.AZURE_OPEN_AI, include_credentials=True)

evaluator_model = {
    "azure_endpoint": connection.endpoint_url,
    "azure_deployment": os.environ["EVALUATION_MODEL"],
    "api_version": "2024-06-01",
    "api_key": connection.key,
}


async def custom_simulator_callback(
    messages: List[Dict],
    stream: bool = False,
    session_state: Any = None,
    context: Optional[Dict[str, Any]] = None,
) -> dict:
    # call your endpoint or ai application here
    actual_messages = messages["messages"]
    print(f"\n🗨️ {actual_messages[-1]['content']}")
    response = chat_with_products(actual_messages)
    message = {
        "role": "assistant",
        "content": response["message"]["content"],
        "context": response["context"]["grounding_data"],
    }
    actual_messages.append(message)
    return {"messages": actual_messages, "stream": stream, "session_state": session_state, "context": context}


async def custom_simulator_raw_conversation_starter():
    outputs = await custom_simulator(
        target=custom_simulator_callback,
        conversation_turns=[
            [
                "I need a new tent, what would you recommend?",
            ],
        ],
        max_conversation_turns=10,
    )
    with open("chat_output.jsonl", "w") as f:
        for output in outputs:
            f.write(output.to_eval_qr_json_lines())


async def evaluate_custom_simulator_raw_conversation_starter():
    coherence_eval = CoherenceEvaluator(model_config=model_config)
    fluency_eval = FluencyEvaluator(model_config=model_config)
    eval_outputs = evaluate(
        data="chat_output.jsonl",
        evaluators={
            "coherence": coherence_eval,
            "fluency": fluency_eval,
        },
        # azure_ai_project=azure_ai_project, # optional only if you did optional installation
    )
    print(eval_outputs)


if __name__ == "__main__":
    custom_simulator = Simulator(model_config=evaluator_model)

    async def main():
        await custom_simulator_raw_conversation_starter()

    asyncio.run(main())
