

# Getting Started

- [Create a personal access token](#create-a-personal-access-token)
- [Install dependencies](#install-depedencies)
- [Set environment variables](#set-environment-variables)
- [Run a basic code sample](#run-a-basic-code-sample)
- [Explore more code snippets](#explore-more-samples)

## 1. Create a personal access token

You'll need to **[create a token](https://github.com/settings/tokens)** to enable free API access. The token will be sent to a Microsoft service but does not need any permissions.

## 2. Install dependencies

Install Azure AI Inferencing package using the following command:

```
WORK IN PROGRESS
```

## 3. Set environment variables
Update or create an environment variable to set your token as the key for the client code.

```bash
export TOKEN="<your-key-goes-here>"

```
Get the model endpoint url and use it in the code below by exporting it as an environment variable

```bash
export MODEL_ENDPOINT="<your-model-endpoint-goes-here>"
```

Set model name in an env variable:

```bash
export MODEL_NAME=Mistral-large
```

## 4. Run a basic code sample

This sample demonstrates a basic call to the chat completion API.
It is leveraging your endpoint and key. The call is synchronous.


```js
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const endpoint = process.env["MODEL_ENDPOINT"];
const token = process.env["TOKEN"];
const modelName = process.env["MODEL_NAME"];

export async function main() {

  const client = new ModelClient(endpoint, new AzureKeyCredential(token));

  const response = await client.path("/chat/completions").post({
    headers: { "x-ms-model-mesh-model-name": modelName }, // NOTE: this is a temporary hotfix
    body: {
      messages: [
        { role:"system", content: "You are a helpful assistant." },
        { role:"user", content: "What is the capital of France?" }
      ],
      model: modelName
    }
  });

  if (response.status !== "200") {
    throw response.body.error;
  }
  console.log(response.body.choices[0].message.content);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```


## 5. Explore more samples

For a better user experience, you will want to stream the response
of the model so that the first token shows up early and you avoid waiting for long responses.


### Run a multi-turn conversation

This sample demonstrates a multi-turn conversation with the chat completion API.
When using the model for a chat application, you'll need to manage the history
of that conversation and send the latest messages to the model.


```python
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const endpoint = process.env["MODEL_ENDPOINT"];
const token = process.env["TOKEN"];
const modelName = process.env["MODEL_NAME"];

export async function main() {

  const client = new ModelClient(endpoint, new AzureKeyCredential(token));

  const response = await client.path("/chat/completions").post({
    headers: { "x-ms-model-mesh-model-name": modelName }, // NOTE: this is a temporary hotfix
    body: {
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "What is the capital of France?" },
        { role: "assistant", content: "The capital of France is Paris." },
        { role: "user", content: "What about Spain?" },
      ],
      model: modelName,
    }
  });

  if (response.status !== "200") {
    throw response.body.error;
  }

  for (const choice of response.body.choices) {
    console.log(choice.message.content);
  }
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```


### Stream the output

For a better user experience, you will want to stream the response
of the model so that the first token shows up early and you avoid waiting for long responses.


```python
import ModelClient from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";
import { createSseStream } from "@azure/core-sse";

const endpoint = process.env["MODEL_ENDPOINT"];
const token = process.env["TOKEN"];
const modelName = process.env["MODEL_NAME"];

export async function main() {

  const client = new ModelClient(endpoint, new AzureKeyCredential(token));

  const response = await client.path("/chat/completions").post({
    headers: { "x-ms-model-mesh-model-name": modelName }, // NOTE: this is a temporary hotfix
    body: {
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "What is the capital of France?" },
      ],
      model: modelName,
      stream: true
    }
  }).asNodeStream();

  const stream = response.body;
  if (!stream) {
    throw new Error("The response stream is undefined");
  }

  if (response.status !== "200") {
    throw new Error(`Failed to get chat completions: ${response.body.error}`);
  }

  const sseStream = createSseStream(stream);

  for await (const event of sseStream) {
    if (event.data === "[DONE]") {
      return;
    }
    for (const choice of (JSON.parse(event.data)).choices) {
      console.log(choice.delta?.content);
    }
  }
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

