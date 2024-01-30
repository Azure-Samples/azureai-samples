## Generate simulated conversation data with your LLM endpoint or local flow

### Overview

This tutorial provides a step-by-step guide on how to leverage Generative AI SDK to generate a simulated conversation using large language models. This example will be useful to developers who need a target test dataset generated that simulates a user persona interacting with a LLM endpoint or local flow you want to test. Large language models are known for their few-shot and zero-shot learning abilities, allowing them to function with minimal data. However, this limited data availability impedes thorough evaluation and optimization when you may not have test datasets to evaluate the quality and effectiveness of your generative AI application. Using large language models such as GPT to simulate a user interaction with your application, with configurable tone, task and characteristics can help with stress testing your application under various environments, effectively gauging how a model responds to different inputs and scenarios.

There are two main uses for generating a simulated interaction (such as as conversation with a chat bot):
- Instance level with manual testing: generate one conversation at a time by manually inputting the task perameters such as name, profile, tone and task and iteratively tweaking it to see different outcomes for the simulated interaction.
- Bulk testing and evaluation orchestration: generate multiple interaction data samples (~100) at one time for a list of tasks or profiles to create an target dataset to evaluate your generative aI applications and streamline the data gathering/prep process.


### Objective

The main objective of this tutorial is to help users understand the process of simulating a conversation with your large langauge model or local flow function. By the end of this tutorial, you should be able to:

 - Configure a conversation template with parameters such as tone, profile and tasks 
 - Simulate a conversation between a user persona you've configured and an endpoint
 - Simulate a conversation between a user persona you've configured and a local flow function. An example chatbot flow has been provided for this example in the `my_chatbot` folder to be referenced in the sample.

Currently `simulator()` supports `conversation` and `summarization` templates for interactions. 

### Programming Languages
 - Python
### Estimated Runtime: 30 mins
