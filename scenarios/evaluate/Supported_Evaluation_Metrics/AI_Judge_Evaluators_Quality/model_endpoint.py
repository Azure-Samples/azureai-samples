from typing_extensions import Self
from typing import TypedDict
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI


class ModelEndpoint:
    def __init__(self: Self, env: dict) -> None:
        self.env = env
        print(self.env)

    class Response(TypedDict):
        query: str
        response: str

    # @trace
    def __call__(self: Self, query: str) -> Response:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=self.env["azure_endpoint"],
            api_version="2024-06-01",
            azure_ad_token_provider=token_provider,
        )
        # Call the model
        completion = client.chat.completions.create(
            model=self.env["azure_deployment"],
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False,
        )
        output = completion.to_dict()
        return {"query": query, "response": output["choices"][0]["message"]["content"]}
