
import requests

from typing import TypedDict
from promptflow.tracing import trace

class ModelEndpoints:

    
    def __init__(self, env, model_type):
        self.env = env
        self.model_type = model_type
        

    class Response(TypedDict):
        question: str
        answer: str

    @trace
    def __call__(self, *, question: str, **kwargs) -> Response:

        if (self.model_type == "tiny_llama"): 
            output = self.call_tiny_llama_endpoint(question)
        elif (self.model_type == "phi3_mini_serverless"):
            output = self.call_phi3_mini_serverless_endpoint(question) 
        elif (self.model_type == "gpt2"):
            output = self.call_gpt2_endpoint(question)  
        elif (self.model_type == 'mistral7b'):
            output = self.call_mistral_endpoint(question)  
        else:
            output = self.call_default_endpoint(question)
        
        return output

    def call_tiny_llama_endpoint(self, question: str, *args, **kwargs) -> Response:

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
        
        answer = output[0]["generated_text"]
        return { "question" : question  , "answer" : answer }

    def call_mistral_endpoint(self, question: str, *args, **kwargs) -> Response:

        endpoint = self.env["mistral7b"]["endpoint"]
        key = self.env["mistral7b"]["key"]

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ key) }

        def query(payload):
            response = requests.post(endpoint, headers=headers, json=payload)
            return response.json()
            
        output = query(
        { 
        "messages": [ 
            { 
            "content": question, 
            "role": "user" 
            } 
        ], 
        "max_tokens": 50
        }
        )
        
        answer = output["choices"][0]["message"]["content"]
        return { "question" : question  , "answer" : answer }

    def call_default_endpoint(question: str, *args, **kwargs) -> Response:
        return { "question" : "What is the capital of France?"  , "answer" : "Paris" }
    
        
	