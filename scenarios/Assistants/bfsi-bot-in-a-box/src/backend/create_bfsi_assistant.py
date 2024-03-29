import logging
from app_config import configure_logger
from pathlib import Path

from create_assistant import clean_assistants, clean_files
from create_assistant import upload_file, create_assistant

from bfsi_config.tools.settings import tools_list
from bfsi_config.tools.settings import assistant_name
from bfsi_config.tools.settings import func_list

configure_logger()


def clean_assistant_data() -> None:
    clean_assistants()
    clean_files()


def create_app_assistant() -> any:
    prompt_file = "bfsi_config/prompts/prompt.txt"
    data_folder = "bfsi_config/data"

    assistant_files = upload_file(data_folder)
    file_ids = list(assistant_files.values())

    with Path(prompt_file).open("r") as file:
        instructions = file.read()

    for filename in assistant_files:
        instructions = instructions.replace(filename, assistant_files[filename])

    logging.info(instructions)

    app_assistant = create_assistant(assistant_name, instructions, tools_list, file_ids)
    assistant_id = app_assistant.id

    return assistant_id, func_list
