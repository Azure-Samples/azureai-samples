
import os
import pathlib
import random
import time
import requests

from typing import List, Tuple, TypedDict
from promptflow.tracing import trace

class TargetEndpointClass:

    def __init__(self, env):
        self.env = env
        # contructor

    class Response(TypedDict):
        question: str
        answer: str

    def __call__(self, question: str, model_type: str) -> Response:
    # def call_external_endpoints(question: str, model_type: str) -> Response:

        if (model_type == "tiny_llama"): 
            output = self.call_tiny_llama_endpoint(question)
        else:
            output = self.call_default_endpoint(question)
        
        print(output)    

        return output

    def call_tiny_llama_endpoint(question: str) -> Response:

        endpoint = env["tiny_llama"]["endpoint"]
        key = env["tiny_llama"]["key"]

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key) }

        print(endpoint)
        print(key)
        print(headers)

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

    def call_phi3_mini_endpoint(question: str) -> str:

        endpoint = env["phi3_mini"]["endpoint"]
        key = env["phi3_mini"]["key"]

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key) }

        print(endpoint)
        print(key)
        print(headers)

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

    def call_default_endpoint(): 
        return { "question" : "What is the capital of France?"  , "answer" : "Paris" }
    
        
	