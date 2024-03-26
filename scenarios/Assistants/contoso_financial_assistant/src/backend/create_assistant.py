# create_assistant.py
import json
import os
import time
from typing import Optional
from pathlib import Path
import base64

from openai import AzureOpenAI
from open_ai_response import client, open_ai_deployment_name


DATA_FOLDER = "./data/"


# add type annotations to the function signature
def upload_file() -> list[str]:
    arr = os.listdir(DATA_FOLDER)
    assistant_files = {}
    my_files = client.files.list()

    for filename in arr:
        found = False
        for prv_file in my_files.data:
            if prv_file.filename == filename:
                print("File already exists: ", filename)
                assistant_files.append(prv_file.id)
                found = True
                break

        if found is False:
            filePath = DATA_FOLDER + filename
            with Path(filePath).open("rb") as f:
                print("Uploading file: ", filePath)
                new_file = client.files.create(file=f, purpose="assistants")
                assistant_files[filename] = new_file.id

    return assistant_files


# In[57]:


# add type annotations to the function signature
def create_assistant(name: str, instructions: str, tools: list, file_ids: list) -> any:
    my_assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    for assistant in my_assistants.data:
        if assistant.name == name:
            return assistant

    return client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model=open_ai_deployment_name,
        file_ids=file_ids,
    )


# add type annotations to the function signature
def create_thread(thread_id: Optional[str] = None) -> any:
    # Create a thread
    if thread_id:
        print("retrieving thread")
        thread = client.beta.threads.retrieve(thread_id)
        if thread:
            print(thread.id)
    else:
        print("creating thread")
        thread = client.beta.threads.create()
        print(thread.id)
    return thread


# add type annotations to the function signature
def clean_assistants() -> None:
    my_assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    for assistant in my_assistants.data:
        print(assistant.id)
        response = client.beta.assistants.delete(assistant.id)
        print(response)


# In[19]:


# add type annotations to the function signature
def clean_files() -> None:
    my_files = client.files.list()
    for file in my_files.data:
        print(file.id)
        response = client.files.delete(file.id)
        print(response)


# In[20]:


def clean_threads() -> None:
    my_threads = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    for thread in my_threads.data:
        print(thread.id)
        response = client.beta.assistants.delete(thread.id)
        print(response)


def create_message(
    client: AzureOpenAI,
    thread_id: str,
    role: str = "",
    content: str = "",
    file_ids: Optional[list] = None,
    metadata: Optional[dict] = None,
    message_id: Optional[str] = None,
) -> any:
    """
    Create a message in a thread using the client.

    @param client: OpenAI client
    @param thread_id: Thread ID
    @param role: Message role (user or assistant)
    @param content: Message content
    @param file_ids: Message file IDs
    @param metadata: Message metadata
    @param message_id: Message ID
    @return: Message object

    """
    if metadata is None:
        metadata = {}
    if file_ids is None:
        file_ids = []

    if client is None:
        print("Client parameter is required.")
        return None

    if thread_id is None:
        print("Thread ID is required.")
        return None

    try:
        if message_id is not None:
            return client.beta.threads.messages.retrieve(
                thread_id=thread_id, message_id=message_id
            )

        if (
            file_ids is not None
            and len(file_ids) > 0
            and metadata is not None
            and len(metadata) > 0
        ):
            return client.beta.threads.messages.create(
                thread_id=thread_id,
                role=role,
                content=content,
                file_ids=file_ids,
                metadata=metadata,
            )

        if file_ids is not None and len(file_ids) > 0:
            return client.beta.threads.messages.create(
                thread_id=thread_id, role=role, content=content, file_ids=file_ids
            )

        if metadata is not None and len(metadata) > 0:
            return client.beta.threads.messages.create(
                thread_id=thread_id, role=role, content=content, metadata=metadata
            )

        return client.beta.threads.messages.create(
            thread_id=thread_id, role=role, content=content
        )

    except Exception as e:
        print(e)
        return None


# add type annotations to the function signature
def get_step_details(run: any, thread: any) -> any:
    arr_retval = []
    arr_stepid = []
    run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
    for run_step in run_steps:
        if run_step.type == "tool_calls":
            for tool in run_step.step_details.tool_calls:
                if tool.type == "function":
                    arr_stepid.append(run_step.id)
                    arr_retval.append(f"Calling {tool.function.name}")
                elif tool.type == "code_interpreter":
                    arr_stepid.append(run_step.id)
                    arr_retval.append("Performing Computations")
                else:
                    arr_retval.append(tool.type)
        else:
            message_id = run_step.step_details.message_creation.message_id
            message = client.beta.threads.messages.retrieve(
                message_id=message_id,
                thread_id=thread.id,
            )
            for msg in message.content:
                if msg.type == "image_file":
                    print(msg.image_file)
                    arr_stepid.append(run_step.id)
                    arr_retval.append("Generating Image")
                else:
                    print(msg.type)
                    arr_stepid.append(run_step.id)
                    arr_retval.append("Creating Message")
    return arr_retval, arr_stepid


def poll_run_till_completion(
    client: AzureOpenAI,
    thread_id: str,
    run_id: str,
    available_functions: dict,
    max_steps: int = 20,
    wait: int = 0.5,
) -> None:
    """
    Poll a run until it is completed or failed or exceeds a certain number of iterations (MAX_STEPS)
    with a preset wait in between polls

    @param client: OpenAI client
    @param thread_id: Thread ID
    @param run_id: Run ID
    @param assistant_id: Assistant ID
    @param verbose: Print verbose output
    @param max_steps: Maximum number of steps to poll
    @param wait: Wait time in seconds between polls

    """
    max_steps = 100
    if (client is None and thread_id is None) or run_id is None:
        print("Client, Thread ID and Run ID are required.")
        return None
    try:
        cnt = 0
        while cnt < max_steps:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            cnt += 1
            print("------------\n")
            print(run.status)
            print("------------\n")
            if run.status == "requires_action":
                print("requires action")
                tool_responses = []
                if (
                    run.required_action.type == "submit_tool_outputs"
                    and run.required_action.submit_tool_outputs.tool_calls is not None
                ):
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls

                    for call in tool_calls:
                        if call.type == "function":
                            # print(call.function.name, available_functions)
                            if call.function.name not in available_functions:
                                raise Exception(
                                    "Function requested by the model does not exist"
                                )
                            function_to_call = available_functions[call.function.name]
                            # print(call.function.arguments)
                            tool_response = function_to_call(
                                **json.loads(call.function.arguments)
                            )
                            # print(tool_response)
                            tool_responses.append(
                                {"tool_call_id": call.id, "output": tool_response}
                            )

                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id, run_id=run.id, tool_outputs=tool_responses
                )
            if run.status == "failed":
                print("Run failed")
                # print(f"Run failed: {run.last_error}")
                print(run)
                return 0
            if run.status == "completed":
                return 1
            time.sleep(wait)
        print("Run exceeded maximum steps:", max_steps)
    except Exception as e:
        print(e)
        return 0


# add type annotations to the function signature
def retrieve_and_print_messages(client: AzureOpenAI, thread_id: str) -> any:
    """
    Retrieve a list of messages in a thread and print it out with the query and response

    @param client: OpenAI client
    @param thread_id: Thread ID
    @param verbose: Print verbose output
    @param out_dir: Output directory to save images
    @return: Messages object

    """
    final_response = []
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        # print(messages)
        for md in reversed(messages.data):
            if md.role == "user":
                # print(final_response)
                final_response = []
                continue

            for mc in md.content:
                # Check if valid text field is present in the mc object
                print("mc.type:", mc.type)
                if mc.type == "text":
                    txt_val = mc.text.value
                    annotations = mc.text.annotations
                    bytes_val = txt_val.encode("utf-8")
                    encoded_val = base64.b64encode(bytes_val).decode("utf-8")
                    final_response.append(
                        {"text_data": encoded_val, "message_id": md.id}
                    )
                    print("\n--------------------")
                    print("mc:", mc)
                    print("\n--------------------")
                    for _index, annotation in enumerate(annotations):
                        # if (file_citation := getattr(annotation, 'file_citation', None)):
                        #    image_data = client.files.content(file_citation.file_id).content
                        if file_path := getattr(annotation, "file_path", None):
                            image_data = client.files.content(file_path.file_id).content
                            encoded_string = base64.b64encode(image_data).decode(
                                "utf-8"
                            )
                            final_response.append(
                                {"img_data": encoded_string, "message_id": md.id}
                            )
                # Check if valid image field is present in the mc object
                elif mc.type == "image_file":
                    print("Found image file")
                    image_data = client.files.content(mc.image_file.file_id).content
                    encoded_string = base64.b64encode(image_data).decode("utf-8")
                    found = False
                    for msg in final_response:
                        if "img_data" in msg and msg["img_data"] == encoded_string:
                            found = True
                            break
                    if not found:
                        final_response.append(
                            {"img_data": encoded_string, "message_id": md.id}
                        )

    except Exception as e:
        print("got error")
        print(e)
        final_response.append({"error_data": e})

    return final_response
