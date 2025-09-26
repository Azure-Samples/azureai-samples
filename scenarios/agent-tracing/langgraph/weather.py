"""
LangGraph single-node weather workflow with Azure tracing.

Env vars required (same as langchain/weather.py):
  AZURE_OPENAI_API_KEY
  AZURE_OPENAI_ENDPOINT
  AZURE_OPENAI_DEPLOYMENT
Optional:
  AZURE_OPENAI_API_VERSION
  APPLICATION_INSIGHTS_CONNECTION_STRING

Run:
  python weather.py
"""

import os
import json
import logging
from datetime import datetime
from typing import TypedDict, List, Annotated, Optional, Any, Dict

from langchain_core.tools import tool
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
    AnyMessage,
)
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import AzureChatOpenAI

try:
    from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer
except ImportError:
    AzureAIOpenTelemetryTracer = None

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("langgraph_weather")


# -----------------------------------------------------------------------------
# Tracing
# -----------------------------------------------------------------------------
_TRACERS: Optional[list[Any]] = None


def setup_tracing() -> list[Any]:
    global _TRACERS
    if _TRACERS is not None:
        return _TRACERS
    tracers: list[Any] = []
    conn = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING")
    if conn and AzureAIOpenTelemetryTracer:
        try:
            tracers.append(
                AzureAIOpenTelemetryTracer(
                    connection_string=conn,
                    enable_content_recording=True,
                    name="langgraph_weather",
                    id="weather_graph_agent",
                    endpoint="weather_graph",
                    scope="LangGraph Weather Flow",
                )
            )
            log.info("Azure tracing enabled.")
        except Exception as e:
            log.warning(f"Tracing init failed: {e}")
    else:
        log.info("Tracing disabled (no APPLICATION_INSIGHTS_CONNECTION_STRING).")
    _TRACERS = tracers
    return tracers


def trace_config(agent_name: str, session_id: str) -> Dict[str, Any]:
    tracers = setup_tracing()
    return {
        "callbacks": tracers,
        "tags": [f"agent:{agent_name}", agent_name, "weather-langgraph"],
        "metadata": {
            "agent_name": agent_name,
            "agent_type": agent_name,
            "langgraph_node": agent_name,
            "session_id": session_id,
            "thread_id": session_id,
            "system": "langgraph-weather",
        },
    }


# -----------------------------------------------------------------------------
# Tool
# -----------------------------------------------------------------------------
@tool
def get_weather(location: str, date: Optional[str] = None) -> str:
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    seed = sum(ord(c) for c in location.lower()) % 4
    conds = ["Sunny", "Windy", "Showers", "Cloudy"]
    cond = conds[seed]
    return json.dumps(
        {
            "location": location,
            "date": date,
            "condition": cond,
            "high_c": 23 + seed,
            "low_c": 13 + seed,
            "advice": "Bring a jacket." if cond != "Sunny" else "Enjoy the sunshine!",
        },
        indent=2,
    )


TOOLS = [get_weather]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


# -----------------------------------------------------------------------------
# State
# -----------------------------------------------------------------------------
class WeatherState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    session_id: str
    done: bool


SYSTEM_PROMPT = """You are a weather assistant.
Use get_weather tool exactly once if user asks about conditions.
Return a concise summary referencing the tool output.
"""


# -----------------------------------------------------------------------------
# LLM
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
        tags=["weather_agent", "weather-langgraph"],
        metadata={
            "agent_type": "weather_agent",
            "agent_name": "weather_agent",
            "system": "langgraph-weather",
            "session_id": session_id,
            "thread_id": session_id,
        },
    )


# -----------------------------------------------------------------------------
# Node
# -----------------------------------------------------------------------------
def weather_node(state: WeatherState) -> WeatherState:
    # If already done, just pass state (idempotency)
    if state.get("done"):
        return state

    llm = build_llm(state["session_id"])
    tool_llm = llm.bind_tools(TOOLS)

    # Step 1: ask the model
    response: AIMessage = tool_llm.invoke(
        state["messages"],
        config=trace_config("weather_agent", state["session_id"]),
    )
    state["messages"].append(response)

    tool_calls = getattr(response, "tool_calls", None)
    if tool_calls:
        # Execute tool calls
        for tc in tool_calls:
            name = tc["name"]
            args = tc.get("args", {})
            tool_obj = TOOLS_BY_NAME.get(name)
            if not tool_obj:
                output = f"Tool '{name}' not found."
            else:
                try:
                    output = tool_obj.invoke(args)
                except Exception as e:
                    output = f"Error executing tool '{name}': {e}"
            state["messages"].append(ToolMessage(name=name, tool_call_id=tc["id"], content=output))
        # After tool outputs, ask model again to summarize
        final_response: AIMessage = llm.invoke(
            state["messages"],
            config=trace_config("weather_agent", state["session_id"]),
        )
        state["messages"].append(final_response)

    # Mark done
    state["done"] = True
    return state


# -----------------------------------------------------------------------------
# Control Flow
# -----------------------------------------------------------------------------
def route(state: WeatherState) -> str:
    if not state.get("done"):
        return "weather_agent"
    return END


def build_app() -> StateGraph:
    g = StateGraph(WeatherState)
    g.add_node("weather_agent", weather_node)
    g.add_conditional_edges(START, lambda _state: "weather_agent")
    g.add_conditional_edges("weather_agent", route)
    checkpointer = MemorySaver()
    return g.compile(checkpointer=checkpointer)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
def main() -> None:
    print("Pure LangGraph Weather (Instrumented)")
    query = input("Ask a weather question: ").strip()
    if not query:
        query = "What's the weather in Lisbon tomorrow?"
    session_id = f"graph-session-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    app = build_app()
    initial: WeatherState = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query),
        ],
        "session_id": session_id,
        "done": False,
    }

    print("\n--- Streaming Steps ---")
    for step in app.stream(initial, {"configurable": {"thread_id": session_id}}):
        print(step)

    final_state = app.get_state({"configurable": {"thread_id": session_id}})
    all_msgs = final_state.values["messages"]
    final_ai = [m for m in all_msgs if isinstance(m, AIMessage)]
    if final_ai:
        print("\n--- Final Answer ---")
        print(final_ai[-1].content)


if __name__ == "__main__":
    main()
