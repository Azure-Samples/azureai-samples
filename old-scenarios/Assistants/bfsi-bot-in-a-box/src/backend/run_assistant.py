import json
import time
from typing import Optional
from base64 import b64encode
import logging
from app_config import configure_logger, client

configure_logger()


def create_thread(thread_id: Optional[str] = None) -> any:
    thread_obj = client.beta.threads
    user_thread = thread_obj.retrieve(thread_id) if thread_id else thread_obj.create()
    return user_thread.id


def create_run(thread_id: str, assistant_id: str) -> any:
    run_obj = client.beta.threads.runs
    run = run_obj.create(thread_id=thread_id, assistant_id=assistant_id)
    return run.id


def create_msg(thread_id: str, role: str, content: str) -> any:
    msg_obj = client.beta.threads.messages
    msg_obj.create(thread_id=thread_id, role=role, content=content)


def process_action(thread_id: str, run_id: any, func_list: dict) -> None:
    run_obj = client.beta.threads.runs
    run = run_obj.retrieve(thread_id=thread_id, run_id=run_id)

    if run.required_action.type != "submit_tool_outputs":
        return

    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    if tool_calls is None:
        return

    tool_responses = []

    for call in tool_calls:
        if call.type == "function":
            if call.function.name not in func_list:
                msg = f"Function does not exist: {call.function.name}"
                raise Exception(msg)
            function_to_call = func_list[call.function.name]
            func_args = json.loads(call.function.arguments)
            tool_response = function_to_call(**func_args)
            resp = {"tool_call_id": call.id, "output": tool_response}
            tool_responses.append(resp)

    run_obj.submit_tool_outputs(
        thread_id=thread_id,  # thread_id
        run_id=run_id,  # run_id
        tool_outputs=tool_responses,  # tool_outputs
    )


def poll_run(thread_id: str, run_id: str, func_list: dict) -> None:
    max_steps = 50
    wait = 5

    try:
        cnt = 0
        run_obj = client.beta.threads.runs
        while cnt < max_steps:
            cnt += 1

            run = run_obj.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == "requires_action":
                process_action(thread_id, run_id, func_list)
            if run.status == "failed":
                logging.info("Run failed")
                return 0
            if run.status == "completed":
                return 1
            time.sleep(wait)
        msg = f"Run exceeded maximum steps: {max_steps}"
        raise Exception(msg)
    except Exception as e:
        logging.info(e)
        return 0


def get_encoded_image(image_data: bytes, msg_id: str) -> dict:
    encoded_string = b64encode(image_data).decode("utf-8")
    return {"img_data": encoded_string, "msg_id": msg_id}


def get_encode_txt(txt_val: str, msg_id: str) -> str:
    bytes_val = txt_val.encode("utf-8")
    encoded_val = b64encode(bytes_val).decode("utf-8")
    return {"text_data": encoded_val, "msg_id": msg_id}


def get_text_msg(msg_text: str, msg_id: str) -> dict:
    txt_val = msg_text.value
    return get_encode_txt(txt_val, msg_id)


def get_msgs(thread_id: str) -> any:
    final_response = []
    try:
        msg_obj = client.beta.threads.messages
        messages = msg_obj.list(thread_id=thread_id)
        img_already_added = False

        for md in reversed(messages.data):
            if md.role == "user":
                final_response = []
                img_already_added = False
                continue

            for mc in md.content:
                if mc.type == "text":
                    final_response.append(get_text_msg(mc.text, md.id))

                    annotations = mc.text.annotations
                    for _index, annotation in enumerate(annotations):
                        if file_path := getattr(annotation, "file_path", None):
                            image_data = client.files.content(file_path.file_id).content
                            final_response.append(get_encoded_image(image_data, md.id))
                            img_already_added = True

                elif mc.type == "image_file":
                    if img_already_added:
                        continue
                    image_data = client.files.content(mc.image_file.file_id).content
                    resp = get_encoded_image(image_data, md.id)
                    final_response.append(resp)

    except Exception as e:
        logging.info(e)
        final_response.append({"error_data": e})

    return final_response


def get_steps(run_id: str, thread_id: str) -> any:
    step_detail_list = []
    step_id_list = []
    run_obj = client.beta.threads.runs
    msg_obj = client.beta.threads.messages
    run_steps = run_obj.steps.list(thread_id=thread_id, run_id=run_id)
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
            msg_id = run_step.step_details.message_creation.message_id
            message = msg_obj.retrieve(message_id=msg_id, thread_id=thread_id)

            for msg in message.content:
                step_id_list.append(run_step.id)
                if msg.type == "image_file":
                    step_detail_list.append("Generating Image")
                else:
                    step_detail_list.append("Creating Message")
    return step_detail_list, step_id_list
