# Generate AI-assisted synthetic data

## Generate Questions and Answers from your data

Large Language Models (LLMs) can help you create question and answer datasets from your existing data sources. These datasets can be useful for various tasks, such as testing your LLM's retrieval capabilities, evaluating and improving your RAG workflows, tuning your prompts and more. In this sample, we will explore how to use the QADataGenerator to generate high-quality questions and answers from your data using LLMs.

This sample will be useful to developers and for data scientists who need data for developing RAG workflows or evaluating and improving RAG workflows.

## Generate simulated conversation data with your chat app or LLM endpoint

Large language models are known for their few-shot and zero-shot learning abilities, allowing them to function with minimal data. However, this limited data availability impedes thorough evaluation and optimization when you may not have test datasets to evaluate the quality and effectiveness of your generative AI application. Using GPT to simulate a user interaction with your application, with configurable tone, task and characteristics can help with stress testing your application under various environments, effectively gauging how a model responds to different inputs and scenarios.

There are two main scenarios for generating a simulated interaction (such as as conversation with a chat bot):
- Instance level with manual testing: generate one conversation at a time by manually inputting the task perameters such as name, profile, tone and task and iteratively tweaking it to see different outcomes for the simulated interaction.
- Bulk testing and evaluation orchestration: generate multiple interaction data samples (~100) at one time for a list of tasks or profiles to create an target dataset to evaluate your generative aI applications and streamline the data gathering/prep process.

This sample will be useful to developers who need a target test dataset generated that simulates a user persona interacting with your chat app or flow.
