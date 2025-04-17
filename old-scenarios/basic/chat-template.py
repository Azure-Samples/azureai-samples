# This file is not meant to be run

# ruff: noqa: E402, ANN201, ANN001

chat = None

# <chat_function>
from azure.ai.inference.prompts import PromptTemplate


def get_chat_response(messages, context):
    # create a prompt template from an inline string (using mustache syntax)
    prompt_template = PromptTemplate.from_string(
        prompt_template="""
        system:
        You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig? Refer to the user by their first name, try to work their last name into a pun.

        The user's first name is {{first_name}} and their last name is {{last_name}}.
        """
    )

    # generate system message from the template, passing in the context as variables
    system_message = prompt_template.create_messages(data=context)

    # add the prompt messages to the user messages
    return chat.complete(
        model="gpt-4o-mini",
        messages=system_message + messages,
        temperature=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )


# </chat_function>

# <create_response>
if __name__ == "__main__":
    response = get_chat_response(
        messages=[{"role": "user", "content": "what city has the best food in the world?"}],
        context={"first_name": "Jessie", "last_name": "Irwin"},
    )
    print(response.choices[0].message.content)
# </create_response>
