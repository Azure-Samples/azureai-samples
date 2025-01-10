from typing import TypedDict
from typing_extensions import Self
import openai
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


class AzureOpenAITarget(object):
    class AzureOpenAITargetResponse(TypedDict):
        response: str

    def __init__(self: Self) -> None:
        self._api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
        self._azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self._azure_deployment = os.environ.get("OPENAI_AZURE_DEPLOYMENT")
        self._model = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

    def __call__(self: Self, *, messages: list) -> AzureOpenAITargetResponse:
        client = openai.AzureOpenAI(
            api_version=self._api_version,
            azure_endpoint=self._azure_endpoint,
            azure_ad_token_provider=get_bearer_token_provider(
                DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
            ),
        )
        response = client.chat.completions.create(
            model=self._model,
            messages=messages,
        )
        response = response.choices[0].message.content
        return {"response": response}
