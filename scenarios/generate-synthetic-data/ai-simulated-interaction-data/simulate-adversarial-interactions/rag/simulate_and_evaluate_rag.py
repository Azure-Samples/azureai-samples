# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from pathlib import Path
import asyncio
from azure.ai.generative.evaluate import evaluate
from azure.ai.resources.client import AIClient
from azure.ai.resources.entities import AzureOpenAIModelConfiguration
from azure.identity import DefaultAzureCredential
from azure.ai.generative.synthetic.simulator import Simulator
from azure.ai.generative.index import get_langchain_retriever_from_index, build_index
from azure.ai.resources.operations import LocalSource, ACSOutputConfig
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI
from langchain import PromptTemplate
from typing import List, Dict, Any, Optional


sub = ""
rg = ""
project_name = ""
os.environ["AZURE_OPENAI_KEY"] = ""
embedding_model_deployment: str = "text-embedding-ada-002"
os.environ["AZURE_OPENAI_ENDPOINT"] = ""
index_name = "product-info-acs-index"
os.environ["AZURE_OPENAI_API_KEY"] = ""
os.environ["AZURE_AI_SEARCH_ENDPOINT"] = ""
os.environ["AZURE_AI_SEARCH_KEY"] = ""


def evaluate_my_data(eval_name: str) -> None:
    # set up your AI client
    client = AIClient(
        subscription_id=sub, resource_group_name=rg, project_name=project_name, credential=DefaultAzureCredential()
    )

    # set up your tracking URL to log results to your project in Azure AI Studio
    tracking_uri = client.tracking_uri
    connection = client.connections.get("Default_AzureOpenAI")
    config = AzureOpenAIModelConfiguration.from_connection(connection, model_name="gpt-4", deployment_name="gpt-4")
    data_path = Path.cwd() / f"\{eval_name}.jsonl"
    output_path = Path.cwd() / "downloaded_artifacts" / "remote"
    result = evaluate(  # This will log metric/artifacts using mlflow
        evaluation_name=eval_name,  # name of your evaluation
        data=data_path,  # get example QA data
        task_type="qa",
        metrics_list=[
            "hate_unfairness",
            "violence",
            "self_harm",
            "sexual",
            "gpt_groundedness",
            "gpt_relevance",
            "gpt_coherence",
            "gpt_fluency",
            "gpt_similarity",
        ],
        model_config=config,
        data_mapping={
            "questions": "question",
            "answer": "answer",
        },
        tracking_uri=tracking_uri,
        output_path=output_path,
    )

    print(result)
    print(result.metrics_summary)  # will print the defect rate for each content harm
    print("Studio URL")
    print(result.studio_url)  # will print the URL to see evaluation results in your Azure AI Studio UI


def build_qna_index() -> None:
    client = AIClient.from_config(DefaultAzureCredential())
    # build the index
    acs_index = build_index(
        output_index_name=index_name,  # name of your index
        vector_store="azure_cognitive_search",  # the type of vector store - in our case it is ACS
        # we are using ada 002 for embedding
        embeddings_model=f"azure_open_ai://deployment/{embedding_model_deployment}/model/{embedding_model_deployment}",
        index_input_config=LocalSource(input_data="data/product-info/"),  # the location of your file/folders
        acs_config=ACSOutputConfig(
            acs_index_name=index_name
            + "-store",  # the name of the index store inside the azure cognitive search service
        ),
    )
    client.indexes.create_or_update(acs_index)


def qna(question: str, temperature: float = 0.5, prompt_template: object = None) -> str:
    # retrieve ML Index from your project
    # this function needs a path. Convert index name to path by adding -mlindex at the end
    index_langchain_retriever = get_langchain_retriever_from_index(index_name + "-mlindex")
    chat_model_deployment: str = "gpt-4"
    llm = AzureChatOpenAI(
        deployment_name=chat_model_deployment,
        model_name=chat_model_deployment,
        temperature=temperature,
        openai_api_version="2023-07-01-preview",
        openai_api_key="",
        azure_endpoint="",
    )

    template = """
    System:
    You are an AI assistant helping users with queries related to outdoor outdoor/camping gear and clothing.
    Use the following pieces of context to answer the questions about outdoor/camping gear and clothing as completely, 
    correctly, and concisely as possible.
    If the question is not related to outdoor/camping gear and clothing, just say Sorry, I only can answer question 
    related to outdoor/camping gear and clothing. So how can I help? Don't try to make up an answer.
    If the question is related to outdoor/camping gear and clothing but vague ask for clarifying questions.
    Do not add documentation reference in the response.

    {context}

    ---

    Question: {question}

    Answer:"
    """
    prompt_template = PromptTemplate(template=template, input_variables=["context", "question"])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=index_langchain_retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt_template,
        },
    )

    response = qa(question)
    return response, temperature


async def qna_as_callback(
    messages: List[Dict],
    stream: bool = False,
    session_state: Any = None,  # noqa: ANN401
    context: Optional[Dict[str, Any]] = None,
) -> dict:
    question = messages["messages"][0]["content"]
    response_from_acs, temperature = qna(question)
    formatted_response = {
        "content": response_from_acs["result"],
        "role": "assistant",
        "context": {
            "temperature": temperature,
            # "source_documents": "\n\n".join([doc.page_content for doc in response_from_acs["source_documents"]])
        },
    }
    messages["messages"].append(formatted_response)
    context = "\n\n".join([doc.page_content for doc in response_from_acs["source_documents"]])

    return {"messages": messages["messages"], "stream": stream, "session_state": session_state, "context": context}


def simulate_data() -> List[Dict]:
    client = AIClient.from_config(DefaultAzureCredential())

    simulator = Simulator.from_fn(fn=qna_as_callback, ai_client=client, model="gpt-4")
    adv_template = Simulator.get_template("adv_qa")
    return asyncio.run(
        simulator.simulate_async(
            adv_template, max_conversation_turns=1, max_simulation_results=6, api_call_delay_sec=10
        )
    )


if __name__ == "__main__":
    build_qna_index()
    result, temperature = qna("Which tent has the highest rainfly waterproof rating?")
    print(result)
    eval_name = "rag-qa-harm-eval-context"
    file_name = f"{eval_name}.jsonl"
    simulation_output = simulate_data()
    jsonl_object = simulation_output.to_eval_qa_json_lines()
    with Path.open(file_name, "w") as f:
        f.write(jsonl_object)

    evaluate_my_data(eval_name)
