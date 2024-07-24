
import os
import pathlib
import random
import time
import requests

from typing import List, Tuple, TypedDict
from promptflow.tracing import trace


class Response(TypedDict):
    question: str
    answer: str

def call_external_endpoints(question: str, model_type: str) -> Response:

    if (model_type == "tiny_llama"): 
        output = call_tiny_llama_endpoint(question)
    elif (model_type == "phi3_mini_serverless"):
        output = call_phi3_mini_serverless_endpoint(question)    
    else:
        output = call_default_endpoint(question)  

    return output

def call_tiny_llama_endpoint(question: str) -> Response:

    # endpoint = os.getenv("TINY_LLAMA_URL")
    # key = os.getenv("TINY_LLAMA_KEY")

    endpoint="https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0/v1/chat/completions"

    headers = {'Content-Type':'application/json', 'Authorization': 'Bearer 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' }

    def query(payload):
        print(payload)
        response = requests.post(endpoint, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "messages": [{
            "role": "user", 
            "content": question
            }],
        "max_tokens": 500,
        "stream": False
        })

    answer = output["choices"][0]["message"]["content"]
    return { "question" : question  , "answer" : answer }

def call_phi3_mini_serverless_endpoint(question: str) -> Response:

    # endpoint = os.getenv("PHI3_MINI_URL")
    # key = os.getenv("PHI3_MINI_KEY")

    endpoint="https://Phi-3-mini-4k-instruct-rqvel.eastus2.models.ai.azure.com/v1/chat/completions"
    key="J6HAqLPf6jyC0ApRXkXRE0cdSpdINcgm"

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key) }

    def query(payload):
        print(payload)
        response = requests.post(endpoint, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "messages": [{
            "role": "user", 
            "content": question
            }],
        "max_tokens": 500
        })
    
    answer = output["choices"][0]["message"]["content"]
    return { "question" : question  , "answer" : answer }

def call_default_endpoint() -> Response: 
    return { "question" : "What is the capital of France?"  , "answer" : "Paris" }

if __name__ == "__main__":
    from dotenv import load_dotenv