# ruff: noqa: E402

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)

# <prompty_chat>
from azure.ai.inference.prompts import PromptTemplate

# load the prompty file and create messages
prompt_template = PromptTemplate.from_prompty("myprompt.prompty")
messages = prompt_template.create_messages(first_name="Jessie", last_name="Irwin")

# run a chat completion using messages and model params from the prompty file
chat = project.inference.get_chat_completions_client()
response = chat.complete(
    messages=messages,
    model=prompt_template.model_name,
    **prompt_template.parameters,
)

print(response.choices[0].message.content)
# </prompty_chat>

assert len(messages) == 2
assert (
    messages[0]["content"]
    == "You are a helpful writing assistant.\nThe user's first name is Jessie and their last name is Irwin."
)
assert messages[0]["role"] == "system"
assert messages[1]["role"] == "user"
