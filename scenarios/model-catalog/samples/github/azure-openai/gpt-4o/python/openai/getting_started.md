

# Getting Started

- [Create a personal access token](#create-a-personal-access-token)
- [Install dependencies](#install-depedencies)
- [Set environment variables](#set-environment-variables)
- [Run a basic code sample](#run-a-basic-code-sample)
- [Explore more code snippets](#explore-more-samples)

## 1. Create a personal access token

You'll need to **[create a token](https://github.com/settings/tokens)** to enable free API access. The token will be sent to a Microsoft service but does not need any permissions.

## 2. Install dependencies

Install OpenAI python package using the following command:

```
pip install openai
```

## 3. Set environment variables
Update or create an environment variable to set your token as the key for the client code.

```bash
export TOKEN="<your-github-token-goes-here>"

```
Get the model endpoint url and use it in the code below by exporting it as an environment variable

```bash
export MODEL_ENDPOINT="<your-model-endpoint-goes-here>"
```

Set model name in an env variable:

```bash
export MODEL_NAME=gpt-4o
```

## 4. Run a basic code sample

This sample demonstrates a basic call to the chat completion API.
It is leveraging your endpoint and key. The call is synchronous.


```python
import os
from openai import OpenAI

endpoint = os.environ["MODEL_ENDPOINT"]
token = os.environ["TOKEN"]
model_name = os.environ["MODEL_NAME"]

client = OpenAI(
    base_url=endpoint,
    api_key=token,
    # NOTE: this is a temporary hotfix
    default_headers={"x-ms-model-mesh-model-name": model_name}
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    model=model_name,
)

print(response.choices[0].message.content)
```


## 5. Explore more samples


### Run a multi-turn conversation

This sample demonstrates a multi-turn conversation with the chat completion API.
When using the model for a chat application, you'll need to manage the history
of that conversation and send the latest messages to the model.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["MODEL_ENDPOINT"]
token = os.environ["TOKEN"]
model_name = os.environ["MODEL_NAME"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
    # NOTE: this is a temporary hotfix
    headers={"x-ms-model-mesh-model-name": model_name},
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    UserMessage(content="What is the capital of France?"),
    AssistantMessage(content="The capital of France is Paris."),
    UserMessage(content="What about Spain?"),
]

response = client.complete(messages=messages, model=model_name)

print(response.choices[0].message.content)
```


### Stream the output

For a better user experience, you will want to stream the response
of the model so that the first token shows up early and you avoid waiting for long responses.


```python
import os
from openai import OpenAI

endpoint = os.environ["MODEL_ENDPOINT"]
token = os.environ["TOKEN"]
model_name = os.environ["MODEL_NAME"]

client = OpenAI(
    base_url=endpoint,
    api_key=token,
    # NOTE: this is a temporary hotfix
    default_headers={"x-ms-model-mesh-model-name": model_name}
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Give me 5 good reasons why I should exercise every day.",
        }
    ],
    model=model_name,
    stream=True
)

for update in response:
    if update.choices[0].delta.content:
        print(update.choices[0].delta.content, end="")
```


### Chat with an image input

This model supports using images as inputs. To run a chat completion
using a local image file, use the following sample:


```python
import os
import base64
from openai import OpenAI

endpoint = os.environ["MODEL_ENDPOINT"]
token = os.environ["TOKEN"]
model_name = os.environ["MODEL_NAME"]

def get_image_data_url(image_file: str, image_format: str) -> str:
    """
    Helper function to converts an image file to a data URL string.

    Args:
        image_file (str): The path to the image file.
        image_format (str): The format of the image file.

    Returns:
        str: The data URL of the image.
    """
    try:
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Could not read '{image_file}'.")
        exit()
    return f"data:image/{image_format};base64,{image_data}"


client = OpenAI(
    base_url=endpoint,
    api_key=token,
    # NOTE: this is a temporary hotfix
    default_headers={"x-ms-model-mesh-model-name": model_name}
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that describes images in details.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": get_image_data_url("sample.png", "png")
                    },
                },
            ],
        },
    ],
    model=model_name,
)

print(response.choices[0].message.content)
```

