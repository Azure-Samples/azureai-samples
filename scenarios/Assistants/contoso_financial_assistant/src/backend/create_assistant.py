import json
import os
import time
from typing import Optional
from pathlib import Path
import base64

from openai import AzureOpenAI
from open_ai_client import client, open_ai_deployment_name

g_assistant = client.beta.assistants
g_messages = client.beta.threads.messages
g_runs = client.beta.threads.runs
g_threads = client.beta.threads


def upload_file(data_folder: str) -> list[str]:
    arr = os.listdir(data_folder)
    assistant_files = {}
    prv_files = client.files.list()

    for filename in arr:
        found = False
        for prv_file in prv_files.data:
            if prv_file.filename == filename:
                assistant_files[filename] = prv_file.id
                found = True
                break

        if found is False:
            with Path(data_folder, filename).open("rb") as f:
                new_file = client.files.create(file=f, purpose="assistants")
                assistant_files[filename] = new_file.id

    return assistant_files


def create_assistant(name: str, instructions: str, tools: list, file_ids: list) -> any:
    my_assistants = g_assistant.list(
        order="desc",
        limit="20",
    )
    for assistant in my_assistants.data:
        if assistant.name == name:
            return assistant

    return g_assistant.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model=open_ai_deployment_name,
        file_ids=file_ids,
    )


def create_thread(thread_id: Optional[str] = None) -> any:
    return g_threads.retrieve(thread_id) if thread_id else g_threads.create()


def clean_assistants() -> None:
    my_assistants = g_assistant.list(
        order="desc",
        limit="20",
    )
    for assistant in my_assistants.data:
        g_assistant.delete(assistant.id)


def clean_files() -> None:
    my_files = client.files.list()
    for file in my_files.data:
        client.files.delete(file.id)


def create_message(thread_id: str, role: str, content: str) -> any:
    try:
        return g_messages.create(thread_id=thread_id, role=role, content=content)
    except Exception as e:
        print(e)
        return None


def get_step_details(run: any, thread: any) -> any:
    step_detail_list = []
    step_id_list = []
    run_steps = g_runs.steps.list(thread_id=thread.id, run_id=run.id)
    for run_step in run_steps:
        if run_step.type == "tool_calls":
            for tool in run_step.step_details.tool_calls:
                step_id_list.append(run_step.id)
                if tool.type == "function":
                    step_detail_list.append(f"Calling {tool.function.name}")
                elif tool.type == "code_interpreter":
                    step_detail_list.append("Performing Computations")
                else:
                    step_detail_list.append(tool.type)
        else:
            message_id = run_step.step_details.message_creation.message_id
            message = g_messages.retrieve(
                message_id=message_id,
                thread_id=thread.id,
            )
            for msg in message.content:
                step_id_list.append(run_step.id)
                if msg.type == "image_file":
                    step_detail_list.append("Generating Image")
                else:
                    step_detail_list.append("Creating Message")
    return step_detail_list, step_id_list


def process_action(thread_id: str, run_id: any, available_functions: dict) -> None:
    run = g_runs.retrieve(thread_id=thread_id, run_id=run_id)
    tool_responses = []
    if (
        run.required_action.type == "submit_tool_outputs"
        and run.required_action.submit_tool_outputs.tool_calls is not None
    ):
        tool_calls = run.required_action.submit_tool_outputs.tool_calls

        for call in tool_calls:
            if call.type == "function":
                if call.function.name not in available_functions:
                    msg = f"Function does not exist: {call.function.name}"
                    raise Exception(msg)
                function_to_call = available_functions[call.function.name]
                func_args = json.loads(call.function.arguments)
                tool_response = function_to_call(**func_args)
                resp = {"tool_call_id": call.id, "output": tool_response}
                tool_responses.append(resp)
    run = g_runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tool_responses)


def poll_run_till_completion(thread_id: str, run_id: str, available_functions: dict) -> None:
    max_steps = 100
    wait = 0.5

    try:
        cnt = 0
        while cnt < max_steps:
            run = g_runs.retrieve(thread_id=thread_id, run_id=run_id)
            cnt += 1

            if run.status == "requires_action":
                process_action(thread_id, run_id, available_functions)
            if run.status == "failed":
                print("Run failed")
                return 0
            if run.status == "completed":
                return 1
            time.sleep(wait)
        print("Run exceeded maximum steps:", max_steps)
    except Exception as e:
        print(e)
        return 0


def retrieve_and_print_messages(client: AzureOpenAI, thread_id: str) -> any:
    final_response = []
    try:
        messages = g_messages.list(thread_id=thread_id)

        for md in reversed(messages.data):
            if md.role == "user":
                final_response = []
                continue

            for mc in md.content:
                img_already_added = False
                if mc.type == "text":
                    txt_val = mc.text.value
                    annotations = mc.text.annotations
                    bytes_val = txt_val.encode("utf-8")
                    encoded_val = base64.b64encode(bytes_val).decode("utf-8")
                    resp = {"text_data": encoded_val, "message_id": md.id}
                    final_response.append(resp)

                    for _index, annotation in enumerate(annotations):
                        if file_path := getattr(annotation, "file_path", None):
                            image_data = client.files.content(file_path.file_id).content
                            encoded_string = base64.b64encode(image_data).decode("utf-8")
                            resp = {"img_data": encoded_string, "message_id": md.id}
                            final_response.append(resp)
                            img_already_added = True

                elif mc.type == "image_file":
                    if img_already_added:
                        continue
                    image_data = client.files.content(mc.image_file.file_id).content
                    encoded_string = base64.b64encode(image_data).decode("utf-8")

                    resp = {"img_data": encoded_string, "message_id": md.id}
                    final_response.append(resp)

    except Exception as e:
        print(e)
        final_response.append({"error_data": e})

    return final_response
