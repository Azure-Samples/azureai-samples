---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Pure LangGraph weather workflow with Azure tracing and single-node tool execution.
---

## Pure LangGraph Weather (Tracing)

### Overview

This sample demonstrates a LangGraph single-node workflow that calls Azure OpenAI chat models and a `get_weather` tool, with traces exported via `langchain-azure-ai` to local OTLP endpoints or Azure Monitor.

### Objective

- Use `langgraph` with `langchain` and Azure OpenAI.
- Instrument with `langchain-azure-ai` and OpenTelemetry for tracing.
- Stream steps and inspect final state in a simple weather flow.

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
- `AZURE_OPENAI_API_VERSION` (optional; defaults to `2024-02-15-preview`)

Optional for tracing:

- `APPLICATION_INSIGHTS_CONNECTION_STRING`

## Run

```
python weather.py
```

Optionally set `OTEL_EXPORTER_OTLP_ENDPOINT` for local OTLP backends, or `APPLICATION_INSIGHTS_CONNECTION_STRING` to send traces to Azure Monitor.
