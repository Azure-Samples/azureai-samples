

# Getting Started

- [Getting Started](#getting-started)
  - [1. Set environment variables](#1-set-environment-variables)
  - [2. Call basic code sample](#2-call-basic-code-sample)
  - [3. Explore more samples](#3-explore-more-samples)
    - [Run a multi-turn conversation](#run-a-multi-turn-conversation)
    - [Stream the output](#stream-the-output)

## 1. Set environment variables
Get the model endpoint url and use it in the code below by exporting it as an environment variable

```bash
export MODEL_ENDPOINT=""
```

Set model name in an env variable:

```bash
export MODEL_NAME=Mistral-small
```

## 2. Call basic code sample

Paste the following into a shell:


```console
TOKEN=$(az account get-access-token --resource=https://ai.azure.com);
curl -X GET "$MODEL_ENDPOINT/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ],
        "model": $MODEL_NAME
    }'
```


## 3. Explore more samples


### Run a multi-turn conversation

Call the chat completion API and pass the chat history:


```console
TOKEN=$(az account get-access-token --resource=https://ai.azure.com);
curl -X GET "$MODEL_ENDPOINT/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "What is the capital of France?"
            },
            {
                "role": "assistant",
                "content": "The capital of France is Paris."
            },
            {
                "role": "user",
                "content": "What about Spain?"
            }
        ],
        "model": $MODEL_NAME
    }'
```


### Stream the output

This is an example of calling the endpoint and streaming the response.


```console
TOKEN=$(az account get-access-token --resource=https://ai.azure.com);
curl -X GET "$MODEL_ENDPOINT/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Give me 5 good reasons why I should exercise every day."
            }
        ],
        "stream": true,
        "model": $MODEL_NAME
    }'
```

