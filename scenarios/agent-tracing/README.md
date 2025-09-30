# Agent Tracing

Reasoning about agent executions is critical for troubleshooting and debugging. Complex agents can involve many nested steps, variable execution paths, and long inputs/outputs, which makes it hard to pinpoint issues. Tracing provides a clear, chronological view of the inputs and outputs for each primitive involved in a run.

This scenario sets up a structure for agent tracing using OpenTelemetry. It supports:
- Local tracing via console or any OTLP-compatible backend (e.g., Aspire Dashboard).
- Cloud tracing via Azure Monitor when Application Insights is enabled for your Azure AI Studio project.

## Structure
- `langchain/`: Tracing patterns for LangChain flows.
- `langgraph/`: Tracing patterns for LangGraph agents/graphs.
- `openai-agents/`: Tracing for OpenAI Agents with Azure OpenAI.
  
Each subfolder contains its own `requirements.txt`, optional `dev-requirements.txt`, and `.env.sample` tailored for that sample.

## Prerequisites
- Python 3.10+ recommended.
- An Azure AI Studio project (optional, for Azure Monitor tracing).
- If using Azure Monitor, enable the Tracing tab in your AI Studio project to provision Application Insights and retrieve the connection string.

## Installation
Navigate to a subfolder and install its `requirements.txt`. Use `dev-requirements.txt` if you want Azure Monitor integrations.

## Configuration
- Local OTLP exporter:
  - Set `OTEL_EXPORTER_OTLP_ENDPOINT` to your backend (e.g., Aspire Dashboard default: `http://localhost:4317` for gRPC, or `http://localhost:4318` for HTTP).
- Azure Monitor:
  - Copy the subfolder `.env.sample` to `.env` and set required values.

## Notes
- The initial release of Azure AI Projects had a known issue where agent function tool call details might be included in traces even when content recording is disabled. Be cautious with sensitive data and review Tracing settings in AI Studio.
