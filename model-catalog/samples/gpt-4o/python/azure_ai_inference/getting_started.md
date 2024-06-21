# Getting Started

- [Create a personal access token](#create-a-personal-access-token)
- [Install dependencies](#install-depedencies)
- [Use your personal access token](#use-your-personal-access-token)
- [Run a basic code sample](#run-a-basic-code-sample)
- [Explore more code snippets](#explore-more-samples)

## 1. Create a personal access token

You'll need this to enable free API access. The token will be sent to a Microsoft service but does not need any permissions.

## 2. Install dependencies

Install Azure AI Inferencing package using the following command:

```
pip install azure-ai-inference
```

## 3. Use your personal access token and get model endpooint

Update or create an environment variable to set your token as the key for the client code.

```bash
export GITHUB_MODELS_API_KEY="<your-key-goes-here>"

```
Get the model endpoint url and use it in the code below by exporting it as an environment variable

```bash
export GITHUB_MODEL_ENDPOINT="<your-model-endpoint-goes-here>"

```

## 4. Run a basic code sample

This sample demonstrates a basic call to the chat completion API.
It is leveraging your endpoint and key. The call is synchronous.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["GITHUB_MODEL_ENDPOINT"]
api_key = os.environ["GITHUB_PAT"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
    headers={"model-name": "gpt-4o"},
)


response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is the capital of France?"),
    ]
)

print(response.choices[0].message.content)
```

## 5. Explore more samples

For a better user experience, you will want to stream the response
of the model so that the first token shows up early and you avoid waiting for long responses.


    ### Run a multi-turn conversation

This sample demonstrates a multi-turn conversation with the chat completion API.
When using the model for a chat application, you'll need to manage the history
of that conversation and send the latest messages to the model.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["GITHUB_MODEL_ENDPOINT"]
api_key = os.environ["GITHUB_PAT"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
    headers={"model-name": "gpt-4o"},
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    UserMessage(content="What is the capital of France?"),
    AssistantMessage(content="The capital of France is Paris."),
    UserMessage(content="What about Spain?"),
]

response = client.complete(messages=messages)

print(response.choices[0].message.content)
```

    ### Stream the output

For a better user experience, you will want to stream the response
of the model so that the first token shows up early and you avoid waiting for long responses.

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["GITHUB_MODEL_ENDPOINT"]
api_key = os.environ["GITHUB_PAT"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
    headers={"model-name": "gpt-4o"},
)

response = client.complete(
    stream=True,
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Give me 5 good reasons why I should exercise every day."),
    ],
)

for update in response:
    print(update.choices[0].delta.content or "", end="")

client.close()
```
