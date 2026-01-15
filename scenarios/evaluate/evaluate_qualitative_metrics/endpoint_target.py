from typing_extensions import Self
from typing import TypedDict
from promptflow.tracing import trace
from openai import AzureOpenAI


class ModelEndpoint:
    def __init__(self: Self, env: dict) -> str:
        self.env = env

    class Response(TypedDict):
        query: str
        response: str

    @trace
    def __call__(self: Self, query: str) -> Response:
        client = AzureOpenAI(
            azure_endpoint=self.env["azure_endpoint"],
            api_version="2024-06-01",
            api_key=self.env["api_key"],
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
