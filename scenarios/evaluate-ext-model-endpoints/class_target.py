
import os
import pathlib
import random
import time
import requests

from typing import List, Tuple, TypedDict
from promptflow.tracing import trace

class ExternalEndpoints:

    
    def __init__(self, env):
        self.env = env
        # contructor

    class Response(TypedDict):
        question: str
        answer: str

    @trace
    def __call__(self, *, question: str, model_type: str, **kwargs) -> Response:

        if (model_type == "tiny_llama"): 
            output = self.call_tiny_llama_endpoint(question)
        elif (model_type == "phi3_mini_serverless"):
            output = self.call_phi3_mini_serverless_endpoint(question) 
        elif (model_type == "gpt2"):
            output = self.call_gpt2_endpoint(question)    
        else:
            output = self.call_default_endpoint(question)
        
        print(output)    

        return output

    def call_tiny_llama_endpoint(self, question: str, *args, **kwargs) -> Response:

        print(self.env["tiny_llama"]["endpoint"])
        print(self.env["tiny_llama"]["key"])

        endpoint = self.env["tiny_llama"]["endpoint"]
        key = self.env["tiny_llama"]["key"]

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key) }

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

    def call_phi3_mini_serverless_endpoint(self, question: str, *args, **kwargs) -> Response:

        endpoint = self.env["phi3_mini_serverless"]["endpoint"]
        key = self.env["phi3_mini_serverless"]["key"]

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

    def call_gpt2_endpoint(self, question: str, *args, **kwargs) -> Response:

        endpoint = self.env["gpt2"]["endpoint"]
        key = self.env["gpt2"]["key"]

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key) }

        def query(payload):
            print(payload)
            response = requests.post(endpoint, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": question,
        })
        
        answer = output["generated_text"]
        return { "question" : question  , "answer" : answer }
    
    def call_default_endpoint(question: str, *args, **kwargs) -> Response:
        return { "question" : "What is the capital of France?"  , "answer" : "Paris" }
    
        
	