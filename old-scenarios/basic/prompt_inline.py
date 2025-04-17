# <inline_prompt>
from azure.ai.inference.prompts import PromptTemplate

# create a prompt template from an inline string (using mustache syntax)
prompt_template = PromptTemplate.from_string(
    prompt_template="""
    system:
    You are a helpful writing assistant.
    The user's first name is {{first_name}} and their last name is {{last_name}}.

    user:
    Write me a short poem about flowers
    """
)

# generate system message from the template, passing in the context as variables
messages = prompt_template.create_messages(first_name="Jessie", last_name="Irwin")


print(messages)

# </inline_prompt>

assert len(messages) == 2
assert (
    messages[0]["content"]
    == "You are a helpful writing assistant.\nThe user's first name is Jessie and their last name is Irwin."
)
assert messages[0]["role"] == "system"
assert messages[1]["role"] == "user"
