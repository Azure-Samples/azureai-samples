import os
from dotenv import load_dotenv
import openai

# Load the environment variables from the .env file
load_dotenv(override=True)

# Retrieve environment variables using os.getenv
open_ai_embedding_endpoint = os.getenv("OPEN_AI_EMBEDDING_ENDPOINT")
open_ai_embedding_key = os.getenv("OPEN_AI_EMBEDDING_KEY")
open_ai_embedding_deployment_name = os.getenv("OPEN_AI_EMBEDDING_DEPLOYMENT_NAME")

open_ai_endpoint = os.getenv("OPEN_AI_ENDPOINT")
open_ai_key = os.getenv("OPEN_AI_KEY")
open_ai_deployment_name = os.getenv("OPEN_AI_DEPLOYMENT_NAME")

client = openai.AzureOpenAI(
    api_key=open_ai_key,
    azure_endpoint=open_ai_endpoint,
    api_version="2024-02-15-preview",
)


def get_embeddings(text: str) -> str:
    # There are a few ways to get embeddings. This is just one example.
    embedding_client = openai.AzureOpenAI(
        api_key=open_ai_embedding_key,
        azure_endpoint=open_ai_embedding_endpoint,
        api_version="2024-02-15-preview",
    )
    depl_model = open_ai_embedding_deployment_name
    embedding = embedding_client.embeddings.create(input=[text], model=depl_model)
    return embedding.data[0].embedding


# add type annotations to the function signature imcluding for max_tokens
def get_response_from_openai(
    query: str, system_content: str, max_tokens: int = 200
) -> str:
    try:
        message_text = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": query},
        ]
        completion = client.chat.completions.create(
            model=open_ai_deployment_name,
            messages=message_text,
            temperature=0.6,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            # response_format={"type": "json_object"},
            stop=None,
        )
        # print(completeion)
        # print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        return {}
