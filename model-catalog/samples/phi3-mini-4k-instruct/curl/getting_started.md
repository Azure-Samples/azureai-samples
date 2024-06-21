# Getting Started

- [Create a personal access token](#create-a-personal-access-token)
- [Use your personal access token](#use-your-personal-access-token)
- [Run a basic code sample](#run-a-basic-code-sample)
- [Explore more code snippets](#explore-more-samples)

## 1. Create a personal access token

You'll need this to enable free API access. The token will be sent to a Microsoft service but does not need any permissions.

## 3. Use your personal access token and get model endpooint

Update or create an environment variable to set your token as the key for the client code.

```bash
export GITHUB_MODELS_API_KEY="<your-key-goes-here>"

```
Get the model endpoint url and use it in the code below by exporting it as an environment variable

```bash
export GITHUB_MODEL_ENDPOINT="<your-model-endpoint-goes-here>"

```

## 4. Call basic code sample

Paste the following into a shell:

```console
curl -X POST "$GITHUB_MODEL_ENDPOINT/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "model-name: gpt-4o" \
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
        ]
    }'
```

## 5. Explore more samples


### Run a multi-turn conversation

Call the chat completion API and pass the chat history:

```console
curl -X POST "$GITHUB_MODEL_ENDPOINT/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "model-name: gpt-4o" \
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
        ]
    }'
```

### Stream the output

This is an example of calling the endpoint and streaming the response.

```console
curl -X POST "$GITHUB_MODEL_ENDPOINT/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "model-name: gpt-4o" \
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
        "stream": true
    }'
```
