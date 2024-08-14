import requests
from typing_extensions import Self
from typing import TypedDict
from promptflow.tracing import trace


class ModelEndpoints:
    def __init__(self: Self, env: dict, model_type: str) -> str:
        self.env = env
        self.model_type = model_type

    class Response(TypedDict):
        question: str
        answer: str

    @trace
    def __call__(self: Self, question: str) -> Response:
        if self.model_type == "gpt4-0613":
            output = self.call_gpt4_endpoint(question)
        elif self.model_type == "gpt35-turbo":
            output = self.call_gpt35_turbo_endpoint(question)
        elif self.model_type == "mistral7b":
            output = self.call_mistral_endpoint(question)
        elif self.model_type == "tiny_llama":
            output = self.call_tiny_llama_endpoint(question)
        elif self.model_type == "phi3_mini_serverless":
            output = self.call_phi3_mini_serverless_endpoint(question)
        elif self.model_type == "gpt2":
            output = self.call_gpt2_endpoint(question)
        else:
            output = self.call_default_endpoint(question)

        return output

    def query(self: Self, endpoint: str, headers: str, payload: str) -> str:
        response = requests.post(url=endpoint, headers=headers, json=payload)
        return response.json()

    def call_gpt4_endpoint(self: Self, question: str) -> Response:
        endpoint = self.env["gpt4-0613"]["endpoint"]
        key = self.env["gpt4-0613"]["key"]

        headers = {"Content-Type": "application/json", "api-key": key}

        payload = {"messages": [{"role": "user", "content": question}], "max_tokens": 500}

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        answer = output["choices"][0]["message"]["content"]
        return {"question": question, "answer": answer}

    def call_gpt35_turbo_endpoint(self: Self, question: str) -> Response:
        endpoint = self.env["gpt35-turbo"]["endpoint"]
        key = self.env["gpt35-turbo"]["key"]

        headers = {"Content-Type": "application/json", "api-key": key}

        payload = {"messages": [{"role": "user", "content": question}], "max_tokens": 500}

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        answer = output["choices"][0]["message"]["content"]
        return {"question": question, "answer": answer}

    def call_tiny_llama_endpoint(self: Self, question: str) -> Response:
        endpoint = self.env["tiny_llama"]["endpoint"]
        key = self.env["tiny_llama"]["key"]

        headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + key)}

        payload = {
            "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 500,
            "stream": False,
        }

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        answer = output["choices"][0]["message"]["content"]
        return {"question": question, "answer": answer}

    def call_phi3_mini_serverless_endpoint(self: Self, question: str) -> Response:
        endpoint = self.env["phi3_mini_serverless"]["endpoint"]
        key = self.env["phi3_mini_serverless"]["key"]

        headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + key)}

        payload = {"messages": [{"role": "user", "content": question}], "max_tokens": 500}

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        answer = output["choices"][0]["message"]["content"]
        return {"question": question, "answer": answer}

    def call_gpt2_endpoint(self: Self, question: str) -> Response:
        endpoint = self.env["gpt2"]["endpoint"]
        key = self.env["gpt2"]["key"]

        headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + key)}

        payload = {
            "inputs": question,
        }

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        answer = output[0]["generated_text"]
        return {"question": question, "answer": answer}

    def call_mistral_endpoint(self: Self, question: str) -> Response:
        endpoint = self.env["mistral7b"]["endpoint"]
        key = self.env["mistral7b"]["key"]

        headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + key)}

        payload = {"messages": [{"content": question, "role": "user"}], "max_tokens": 50}

        output = self.query(endpoint=endpoint, headers=headers, payload=payload)
        answer = output["choices"][0]["message"]["content"]
        return {"question": question, "answer": answer}

    def call_default_endpoint(question: str) -> Response:
        return {"question": "What is the capital of France?", "answer": "Paris"}
