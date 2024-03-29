from flask import Flask, request
from flask_cors import CORS
import logging
from app_config import configure_logger
from create_bfsi_assistant import create_app_assistant
from run_assistant import create_thread, create_msg, create_run
from run_assistant import get_steps, poll_run, get_msgs

configure_logger()

g_cache = {}

g_assistant_id, func_list = create_app_assistant()


def get_answer_for_query(user_query: str, thread_id: str) -> dict:
    thread_id = create_thread(thread_id)

    message_role = "user"
    create_msg(thread_id, message_role, user_query)

    run_id = create_run(thread_id, g_assistant_id)

    run_status = poll_run(thread_id, run_id, func_list)

    if run_status == 1:
        messages = get_msgs(thread_id)
    else:
        messages = []
        logging.info("error in getting answer for query")

    return {"messages": messages, "thread_id": thread_id, "run_id": run_id}


def get_answer_from_cache(query: str, thread_id: str) -> dict:
    if thread_id == "":
        return None
    if thread_id in g_cache:
        thread_catch = g_cache[thread_id]
        if query in thread_catch:
            return thread_catch[query]
        return None
    return None


def set_answer_to_cache(query: str, thread_id: str, response: dict) -> None:
    if thread_id not in g_cache:
        g_cache[thread_id] = {}
    g_cache[thread_id][query] = response


app = Flask(__name__)
CORS(app)


@app.route("/get_step", methods=["POST"])
def api_get_step() -> dict:
    thread_id = request.form.get("thread_id")
    run_id = request.form.get("run_id")

    if thread_id == "":
        return None

    step_detail_list, step_id_list = get_steps(run_id, thread_id)
    return {"step_detail_list": step_detail_list, "step_id_list": step_id_list}


@app.route("/get_answer", methods=["POST"])
def api_get_answer() -> dict:
    query = request.form.get("query")
    thread_id = request.form.get("thread_id")

    response = get_answer_from_cache(query, thread_id)
    if response is not None:
        return response

    response = get_answer_for_query(query, thread_id)
    set_answer_to_cache(query, thread_id, response)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
