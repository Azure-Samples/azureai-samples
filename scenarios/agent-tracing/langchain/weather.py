"""
LangChain Weather Assistant with manual tool-calling loop + Azure tracing.

Env vars required:
  AZURE_OPENAI_API_KEY=...
  AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
  AZURE_OPENAI_DEPLOYMENT=yourDeploymentName
  AZURE_OPENAI_API_VERSION=2024-02-15-preview  (or compatible)

Optional tracing:
  APPLICATION_INSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...

Run:
  python weather.py
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Any, Optional, Dict

from langchain_core.tools import tool
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    BaseMessage,
)
from langchain_openai import AzureChatOpenAI

try:
    from langchain_azure_ai.callbacks.tracers import AzureAIInferenceTracer
except ImportError:
    AzureAIInferenceTracer = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langchain_weather")


# -----------------------------------------------------------------------------
# Tracing Setup (cached)
# -----------------------------------------------------------------------------
_TRACERS: Optional[List[Any]] = None


def setup_tracing() -> List[Any]:
    global _TRACERS
    if _TRACERS is not None:
        return _TRACERS
    tracers: List[Any] = []
    conn = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING")
    if conn and AzureAIInferenceTracer:
        try:
            tracer = AzureAIInferenceTracer(
                connection_string=conn,
                enable_content_recording=True,
                name="langchain_weather",
                id="weather_agent",
                endpoint="weather_single",
                scope="Pure LangChain Weather",
            )
            tracers.append(tracer)
            logger.info("Azure tracing enabled.")
        except Exception as e:
            logger.warning(f"Failed to init tracer: {e}")
    else:
        logger.info("Tracing not enabled (missing APPLICATION_INSIGHTS_CONNECTION_STRING or dependency).")
    _TRACERS = tracers
    return tracers


def trace_config(agent_name: str, session_id: str) -> Dict[str, Any]:
    tracers = setup_tracing()
    return {
        "callbacks": tracers,
        "tags": [f"agent:{agent_name}", agent_name, "weather-langchain"],
        "metadata": {
            "agent_name": agent_name,
            "agent_type": agent_name,
            "langgraph_node": agent_name,  # kept for parity
            "session_id": session_id,
            "thread_id": session_id,
            "system": "langchain-weather",
        },
    }


# -----------------------------------------------------------------------------
# Tool
# -----------------------------------------------------------------------------
@tool
def get_weather(location: str, date: Optional[str] = None) -> str:
    """
    Return a mock weather forecast as JSON.
    """
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    seed = sum(ord(c) for c in location.lower()) % 5
    conditions = ["Sunny", "Partly Cloudy", "Light Rain", "Overcast", "Showers"]
    cond = conditions[seed]
    forecast = {
        "location": location,
        "date": date,
        "condition": cond,
        "temp_high_c": 24 + seed,
        "temp_low_c": 14 + seed,
        "advice": "Great day outside!" if cond == "Sunny" else "Plan for changing conditions.",
    }
    return json.dumps(forecast, indent=2)


TOOLS = [get_weather]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


# -----------------------------------------------------------------------------
# LLM Factory
# -----------------------------------------------------------------------------
def build_llm(session_id: str) -> AzureChatOpenAI:
    required = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT",
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing Azure OpenAI env vars: {', '.join(missing)}")
    return AzureChatOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        temperature=0.2,
        callbacks=setup_tracing(),
        tags=["weather_agent", "weather-langchain"],
        metadata={
            "agent_type": "weather_agent",
            "agent_name": "weather_agent",
            "system": "langchain-weather",
            "session_id": session_id,
            "thread_id": session_id,
        },
    )


SYSTEM_PROMPT = """You are a weather assistant.
If user asks about weather, call the get_weather tool with (location, date if given).
If ambiguous date, assume tomorrow.
After tool output, summarize succinctly for the user.
"""


# -----------------------------------------------------------------------------
# Agent Loop (manual)
# -----------------------------------------------------------------------------
def run_weather_conversation(user_query: str, session_id: str) -> str:
    llm = build_llm(session_id)
    # Bind tools for tool-calling (function-calling) capability
    tool_llm = llm.bind_tools(TOOLS)

    messages: List[BaseMessage] = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query),
    ]

    # We allow up to N reasoning/tool steps (simple guard)
    for step in range(5):
        logger.info(f"LLM step {step + 1}")
        response: AIMessage = tool_llm.invoke(messages, config=trace_config("weather_agent", session_id))
        messages.append(response)

        # If the model decided not to call any tools, we stop
        tool_calls = getattr(response, "tool_calls", None)
        if not tool_calls:
            logger.info("No tool calls; finishing.")
            break

        # Execute each tool call and append ToolMessage
        for tc in tool_calls:
            name = tc["name"]
            args = tc.get("args", {})
            tool_obj = TOOLS_BY_NAME.get(name)
            if not tool_obj:
                tool_output = f"Tool '{name}' not found."
            else:
                try:
                    tool_output = tool_obj.invoke(args)
                except Exception as e:
                    tool_output = f"Error executing tool '{name}': {e}"
            messages.append(
                ToolMessage(
                    content=tool_output,
                    name=name,
                    tool_call_id=tc["id"],
                )
            )

    # Final answer: last AI message with no tool calls OR last AI message overall
    final_ai = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
    return final_ai.content if final_ai else "No AI response."


def main() -> None:
    print("Pure LangChain Weather (Instrumented)")
    q = input("Ask a weather question (e.g. 'Weather in Tokyo tomorrow'): ").strip()
    if not q:
        q = "Weather in Paris"
    session_id = f"lc-session-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    answer = run_weather_conversation(q, session_id)
    print("\n--- Answer ---")
    print(answer)


if __name__ == "__main__":
    main()
