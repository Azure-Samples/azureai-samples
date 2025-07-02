---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluate.
---

## Evaluate

### Overview

This tutorial provides a step-by-step guide on how to evaluate Generative AI base models or AI Applications with Azure. Each of these samples uses the [`azure-ai-evaluation`](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/evaluate-sdk) SDK. 

When selecting a base model for building an application—or after building an AI application (such as a Retrieval-Augmented Generation (RAG) system or a multi-agent framework)—evaluation plays a pivotal role. Effective evaluation ensures that the chosen or developed AI model or application meets the intended safety, quality, and performance benchmarks.

In both cases, running evaluations requires specific tools, methods, and datasets. Here’s a breakdown of the key components involved:

* Testing with Evaluation Datasets

    - Bring Your Own Data: Use datasets tailored to your application or domain.
    - Redteaming Queries: Design adversarial prompts to test robustness.
    - [Azure AI Simulators](Simulators/): Leverage Azure AI's context-specific or adversarial dataset generators to create relevant test cases.

* Selecting the Appropriate Evaluators or Building Custom Ones

    - Pre-Built Evaluators: Azure AI provides a range of [generation safety](Supported_Evaluation_Metrics/AI_Judge_Evaluators_Safety_Risks/) and [quality/NLP evaluators](Supported_Evaluation_Metrics/AI_Judge_Evaluators_Quality/) ready for immediate use.
    - [Custom Evaluators](Supported_Evaluation_Metrics/Custom_Evaluators/): Using the Azure AI Evaluation SDK, you can design and implement evaluators that align with the unique requirements of your application.

* Generating and Visualizing Evaluation Results: Azure AI Evaluation SDK enables you to evaluate the target functions (such as [endpoints of your AI application](Supported_Evaluation_Targets/Evaluate_App_Endpoint/) or your [model endpoints](Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/) on your dataset with either built-in or custom evaluators. You can run evaluations [remotely](Supported_Evaluation_Targets/Evaluate_On_Cloud/) in the cloud or locally on your own machine.

### Objective

The main objective of this tutorial is to help users understand the process of evaluating an AI model in Azure. By the end of this tutorial, you should be able to:

 - Simulate interactions with an AI model 
 - Evaluate both deployed model endpoints and applications
 - Evaluate using quantitative NLP metrics, qualitative metrics, and custom metrics

 Our samples cover the following tools for evaluation of AI models in Azure:  

| Sample name                            | adversarial | simulator | conversation starter | index | raw text | against model endpoint | against app | qualitative metrics | custom metrics | quantitative NLP metrics |
|----------------------------------------|-------------|-----------|---------------------|-------|----------|-----------------------|-------------|---------------------|----------------|----------------------|
| [Simulate_Adversarial.ipynb](Simulators/Simulate_Adversarial_Data/Simulate_Adversarial.ipynb)           | X           | X         |                     |      |          | X                      |             |                     |                |                      |
| [Simulate_From_Conversation_Starter.ipynb](Simulators/Simulate_Context-Relevant_Data/Simulate_From_Conversation_Starter/Simulate_From_Conversation_Starter.ipynb)   |             | X         | X                   |       |         | X                      |             |                     |                |                      |
| [Simulate_From_Azure_Search_Index.ipynb](Simulators/Simulate_Context-Relevant_Data/Simulate_From_Azure_Search_Index/Simulate_From_Azure_Search_Index.ipynb)            |             | X         |                     | X     |          | X                      |             |                     |                |                      |
| [Simulate_From_Input_Text.ipynb](Simulators/Simulate_Context-Relevant_Data/Simulate_From_Input_Text/Simulate_From_Input_Text.ipynb)             |             | X         |                     |       | X        | X                     |             |                     |                |                      |
| [Evaluate_Base_Model_Endpoint.ipynb](Supported_Evaluation_Targets/Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb)              |             |           |                     |      |          | X                      |            | X                    |                |                      |
| [Evaluate_App_Endpoint.ipynb](Supported_Evaluation_Targets/Evaluate_App_Endpoint/Evaluate_App_Endpoint.ipynb)                    |             |           |                     |       |         |                       | X           | X                    |                |                      |
| [AI_Judge_Evaluators_Quality.ipynb](Supported_Evaluation_Metrics/AI_Judge_Evaluators_Quality/AI_Judge_Evaluators_Quality.ipynb)            |             |           |                     |       |         | X                      |            | X                    |                |                      |
| [Custom_Evaluators_Privacy.ipynb](Supported_Evaluation_Metrics/Custom_Evaluators/Custom_Evaluators_Privacy/Custom_Evaluators_Privacy.ipynb)                |             |           |                     |       |         | X                      |            |                     | X               |                      |
| [Custom_Evaluators_Blocklisting.ipynb](Supported_Evaluation_Metrics/Custom_Evaluators/Custom_Evaluators_Blocklisting/Custom_Evaluators_Blocklisting.ipynb)                |             |           |                     |       |         | X                      |            |                     | X               |                      |
| [NLP_Evaluators.ipynb](Supported_Evaluation_Metrics/NLP_Evaluators/NLP_Evaluators.ipynb)            |             |           |                     |       |         | X                      |             |                     |               | X                     |
| [AI_Judge_Evaluators_Safety_Risks.ipynb](Supported_Evaluation_Metrics/AI_Judge_Evaluators_Safety_Risks/AI_Judge_Evaluators_Safety_Risks_Text.ipynb)            | X           |           |                     |       |          | X                     |             |                     |                |                      |
| [Simulate_Evaluate_Groundedness.py](Simulators/Simulate_Evaluate_Groundedness/Simulate_Evaluate_Groundedness.ipynb)      |             | X         |                     |      | X        | X                     |             | X                    |                |                    |
| [Azure_OpenAI_Graders.ipynb](Azure_OpenAI_Graders/Azure_OpenAI_Graders.ipynb)      |             |           |                     |      | X        | X                     |             | X                    |                |                    |



### Pre-requisites
To use the `azure-ai-evaluation` SDK, install with```python pip install azure-ai-evaluation``` Python 3.8 or later is required to use this package.- See our Python reference documentation for our `azure-ai-evaluation` SDK[here](https://aka.ms/azureaieval-python-ref) for more granular details on input/output requirements and usage instructions.- Check out our Github repo for `azure-ai-evaluation` SDK [here](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation). 


### Programming Languages
 - Python

### Estimated Runtime: 30 mins
