from flask import Flask, request
from flask_cors import CORS
import json
from pathlib import Path

from assistant_config.tools import tools_list, available_functions

from create_assistant import clean_assistants, clean_files
from create_assistant import (
    upload_file,
    create_assistant,
    create_thread,
    create_message,
)
from create_assistant import (
    get_step_details,
    poll_run_till_completion,
    retrieve_and_print_messages,
)
from open_ai_client import client


g_runs = client.beta.threads.runs
g_threads = client.beta.threads

g_cache = {}


def get_answer_for_query(user_query: str, thread_id: str) -> dict:
    message_role = "user"
    thread = create_thread(thread_id)
    thread_id = thread.id
    create_message(thread_id, message_role, user_query)

    run = g_runs.create(thread_id=thread_id, assistant_id=g_assistant.id)
    status = poll_run_till_completion(
        thread_id=thread_id,
        run_id=run.id,
        available_functions=available_functions,
    )

    if status == 1:
        messages = retrieve_and_print_messages(client=client, thread_id=thread_id)
    else:
        messages = []
        print("error in getting answer for query")

    return {"messages": messages, "thread_id": thread_id, "run_id": run.id}


def get_answer_from_cache(query: str, thread_id: str) -> dict:
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


def init_assistant() -> any:
    clean_assistants()
    clean_files()

    config_file = "assistant_config/config.json"
    prompt_file = "assistant_config/prompt.txt"
    data_folder = "assistant_data"

    with Path(config_file).open("r") as f:
        config = json.load(f)
        assistant_name = config["assistant_name"]

    assistant_files = upload_file(data_folder)
    file_ids = list(assistant_files.values())

    with Path(prompt_file).open("r") as file:
        instructions = file.read()

    for filename in assistant_files:
        instructions = instructions.replace(filename, assistant_files[filename])

    print(instructions)

    return create_assistant(assistant_name, instructions, tools_list, file_ids)


g_assistant = init_assistant()
app = Flask(__name__)
CORS(app)


# add type annotations to the function signature
@app.route("/get_step", methods=["POST"])
def api_get_step() -> dict:
    thread_id = request.form.get("thread_id")
    run_id = request.form.get("run_id")

    if thread_id == "":
        return None

    run = g_runs.retrieve(thread_id=thread_id, run_id=run_id)
    thread = g_threads.retrieve(thread_id)
    step_detail_list, step_id_list = get_step_details(run, thread)
    return {"step_detail_list": step_detail_list, "step_id_list": step_id_list}


@app.route("/get_answer", methods=["POST"])
def api_get_answer() -> dict:
    query = request.form.get("query")

    thread_id = request.form.get("thread_id")
    thread_id = thread_id if thread_id != "" else None

    response = get_answer_from_cache(query, thread_id)
    if response is not None:
        return response

    response = get_answer_for_query(query, thread_id)
    set_answer_to_cache(query, thread_id, response)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
