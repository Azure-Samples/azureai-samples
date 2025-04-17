import logging
from app_config import configure_logger, client, open_ai_deployment_name
from pathlib import Path
import os

configure_logger()


def clean_assistants() -> None:
    my_assistants = client.beta.assistants.list(order="desc", limit="20")
    for assistant in my_assistants.data:
        client.beta.assistants.delete(assistant.id)


def clean_files() -> None:
    my_files = client.files.list()
    for file in my_files.data:
        logging.info(file.id, file.filename)
        client.files.delete(file.id)


def upload_file(data_folder: str) -> list[str]:
    data_files = os.listdir(data_folder)
    assistant_files = {}
    prv_files = client.files.list()

    for filename in data_files:
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
    my_assistants = client.beta.assistants.list(order="desc", limit="20")
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
