---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Pure LangChain weather assistant with Azure tracing and manual tool-calling loop.
---

## Pure LangChain Weather (Tracing)

### Overview

This sample demonstrates a pure LangChain agent that uses a manual tool-calling loop, instrumented with Azure Application Insights via `langchain-azure-ai`. It calls Azure OpenAI chat models and a simple `get_weather` tool, and emits OpenTelemetry traces locally or to Azure Monitor.

### Objective

- Use `langchain` and `langchain-openai` with Azure OpenAI chat models.
- Add tracing via `langchain-azure-ai` and OpenTelemetry.
- Implement a manual tool-calling loop for clarity and control.

### Programming Languages

- Python

### Estimated Runtime: 10 mins

## Set up

Create and activate a local virtual environment, then install dependencies:

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

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION` (default `2024-02-15-preview`)

Optional for tracing:

- `APPLICATION_INSIGHTS_CONNECTION_STRING`

## Run

```
python weather.py
```

You can send traces to an OTLP-compatible backend by setting `OTEL_EXPORTER_OTLP_ENDPOINT`, or to Azure Monitor by setting `APPLICATION_INSIGHTS_CONNECTION_STRING`.
