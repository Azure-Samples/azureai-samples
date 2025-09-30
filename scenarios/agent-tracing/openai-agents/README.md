---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: OpenAI Agents sample (Spanish Tutor) instrumented with OpenTelemetry for console or Azure Monitor.
---

## OpenAI Agents Spanish Tutor (Tracing)

### Overview

This sample uses the `openai-agents` Python SDK with Azure OpenAI (Chat Completions) and instruments agent runs via OpenTelemetry. It authenticates using `DefaultAzureCredential` (supports `az login` or service principal) and exports spans either to Azure Monitor or the console.

### Objective

- Configure Azure OpenAI with the `openai` SDK and `openai-agents`.
- Instrument the Agents framework with `opentelemetry-instrumentation-openai-agents`.
- Export traces to Azure Monitor or console.

### Programming Languages

- Python

### Estimated Runtime: 10 mins

## Set up

Create a virtual environment and install dependencies:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Copy the environment template and set required variables:

```
cp .env.sample .env
```

Required:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_VERSION`
- `AZURE_OPENAI_CHAT_DEPLOYMENT`

Optional tracing:

- `APPLICATION_INSIGHTS_CONNECTION_STRING`

## Run

```
API_HOST=azure python spanish_tutor.py
```

Provide `APPLICATION_INSIGHTS_CONNECTION_STRING` to export traces to Azure Monitor, otherwise spans are printed to console. Ensure you have `az login` or a valid service principal configured for `DefaultAzureCredential`.
