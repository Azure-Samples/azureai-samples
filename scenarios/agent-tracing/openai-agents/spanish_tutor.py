"""
Spanish Tutor (Azure OpenAI) + OpenTelemetry (Console or Azure Monitor)

This script:
  * Uses Azure OpenAI (Chat Completions) via the `openai` Python SDK (>=1.x)
  * Authenticates with DefaultAzureCredential (so you can use az login or a service principal)
  * Instruments the OpenAI Agents framework with OpenTelemetry
  * Captures rich GenAI semantic attributes (messages, system instructions, tool definitions)
  * Exports spans either to:
        - Azure Monitor (if APPLICATION_INSIGHTS_CONNECTION_STRING is set), or
        - Console (fallback)

Prerequisites:
  pip install:
    openai
    openai-agents
    azure-identity
    opentelemetry-sdk
    opentelemetry-api
    opentelemetry-instrumentation-openai-agents
    (optional) azure-monitor-opentelemetry-exporter

Run:
  API_HOST=azure  python spanish_tutor.py
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

import azure.identity
import openai
from agents import Agent, OpenAIChatCompletionsModel, Runner  # from openai-agents

from opentelemetry import trace
from opentelemetry.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

logging.basicConfig(level=logging.INFO)


@dataclass
class _ApiConfig:
    build_client: Callable[[], openai.AsyncAzureOpenAI]
    model_name: str
    base_url: str
    provider: str


def _set_capture_env(_provider: str, base_url: str) -> None:
    """
    Set OpenTelemetry + GenAI semantic capture environment toggles if not already provided.
    These default to 'true' to showcase the richest possible trace payload.
    """
    capture_defaults = {
        # Enable instrumentation features
        "OTEL_INSTRUMENTATION_OPENAI_AGENTS_CAPTURE_CONTENT": "true",
        "OTEL_INSTRUMENTATION_OPENAI_AGENTS_CAPTURE_METRICS": "true",
        # Generic GenAI semantic attrs capture
        "OTEL_GENAI_CAPTURE_MESSAGES": "true",
        "OTEL_GENAI_CAPTURE_SYSTEM_INSTRUCTIONS": "true",
        "OTEL_GENAI_CAPTURE_TOOL_DEFINITIONS": "true",
        "OTEL_GENAI_EMIT_OPERATION_DETAILS": "true",
        # Agent identity metadata
        "OTEL_GENAI_AGENT_NAME": os.getenv("OTEL_GENAI_AGENT_NAME", "Spanish Tutor Agent"),
        "OTEL_GENAI_AGENT_DESCRIPTION": os.getenv(
            "OTEL_GENAI_AGENT_DESCRIPTION",
            "Conversational tutor that always replies in Spanish",
        ),
        "OTEL_GENAI_AGENT_ID": os.getenv("OTEL_GENAI_AGENT_ID", "spanish-tutor"),
    }
    for k, v in capture_defaults.items():
        os.environ.setdefault(k, v)

    # 'provider' is used for identity metadata in env; parsing base_url sets server attrs
    parsed = urlparse(base_url)
    if parsed.hostname:
        os.environ.setdefault("OTEL_GENAI_SERVER_ADDRESS", parsed.hostname)
    if parsed.port:
        os.environ.setdefault("OTEL_GENAI_SERVER_PORT", str(parsed.port))


def _resolve_api_config() -> _ApiConfig:
    """
    For this Azure-focused sample we expect API_HOST=azure.
    """
    host = os.getenv("API_HOST", "azure").lower()
    if host != "azure":
        raise ValueError("This sample is locked to API_HOST=azure for clarity.")

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    api_version = os.environ["AZURE_OPENAI_VERSION"]
    deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

    credential = azure.identity.DefaultAzureCredential()
    token_provider = azure.identity.get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default",
    )

    def _build_client() -> openai.AsyncAzureOpenAI:
        return openai.AsyncAzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
        )

    return _ApiConfig(
        build_client=_build_client,
        model_name=deployment,
        base_url=endpoint,
        provider="azure.ai.openai",
    )


def _configure_otel() -> None:
    """
    Configure TracerProvider + exporter.
    If APPLICATION_INSIGHTS_CONNECTION_STRING is set, export to Azure Monitor.
    Otherwise, export spans to the console.
    """
    conn = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING")
    resource = Resource.create(
        {
            "service.name": os.getenv("OTEL_SERVICE_NAME", "spanish-tutor-app"),
            "service.namespace": "language-learning",
            "service.version": os.getenv("SERVICE_VERSION", "1.0.0"),
        }
    )

    tracer_provider = TracerProvider(resource=resource)

    if conn:
        try:
            from azure.monitor.opentelemetry.exporter import (  # type: ignore
                AzureMonitorTraceExporter,
            )
        except ImportError:
            print(
                "Azure Monitor exporter not installed. Falling back to console. "
                "Install with: pip install azure-monitor-opentelemetry-exporter"
            )
            tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        else:
            tracer_provider.add_span_processor(
                BatchSpanProcessor(AzureMonitorTraceExporter.from_connection_string(conn))
            )
            print("[otel] Azure Monitor trace exporter configured")
    else:
        tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        print("[otel] Console span exporter configured")
        print("[otel] Provide APPLICATION_INSIGHTS_CONNECTION_STRING to export to Azure Monitor.")

    trace.set_tracer_provider(tracer_provider)


def _infer_span_name(provider: str) -> str:
    return f"spanish_tutor_session[{provider}]"


async def main() -> None:
    api_config = _resolve_api_config()
    _set_capture_env(api_config.provider, api_config.base_url)
    _configure_otel()

    # Instrument AFTER setting tracer provider
    OpenAIAgentsInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())

    client = api_config.build_client()

    agent = Agent(
        name="Spanish tutor",
        instructions="You are a Spanish tutor. Help the user learn Spanish. ONLY respond in Spanish.",
        model=OpenAIChatCompletionsModel(
            model=api_config.model_name,
            openai_client=client,
        ),
    )

    tracer = trace.get_tracer(__name__)
    # Create a session span
    with tracer.start_as_current_span(_infer_span_name(api_config.provider)):
        result = await Runner.run(agent, input="Hola, ¿cómo estás?")
        print("\n=== Final Tutor Reply (Spanish) ===")
        print(result.final_output)
        print("==================================\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        # Ensure processors flush
        trace.get_tracer_provider().shutdown()
