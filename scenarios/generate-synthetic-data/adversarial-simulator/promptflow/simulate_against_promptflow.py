# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# pylint: skip-file
import asyncio
from azure.ai.resources.client import AIClient
from azure.ai.resources.entities import AzureOpenAIModelConfiguration
from azure.identity import DefaultAzureCredential
import json
from azure.ai.generative.synthetic.simulator import Simulator

credential = DefaultAzureCredential()
client = AIClient.from_config(credential)

userbot_config = AzureOpenAIModelConfiguration.from_connection(
    connection=client.get_default_aoai_connection(),
    model_name="gpt-4",
    deployment_name="gpt-4",
    max_tokens=300,
    temperature=0.0,
)

template = Simulator.get_template("adv_conversation")

simulator = Simulator.from_pf_path(
    pf_path="./my_chatbot",
    ai_client=client,
)

outputs = asyncio.run(simulator.simulate_async(template=template, max_conversation_turns=2))

for line in outputs:
    print(json.dumps(line, indent=2))
in_json_line_format = outputs.to_json_lines()
