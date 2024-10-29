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

This tutorial provides a step-by-step guide on how to evaluate Generative AI models with Azure. Each of these samples uses the `azure-ai-evaluation` SDK. 

### Objective

The main objective of this tutorial is to help users understand the process of evaluating an AI model in Azure. By the end of this tutorial, you should be able to:

 - Simulate interactions with an AI model 
 - Evaluate both deployed model endpoints and applications
 - Evaluate using quantitative NLP metrics, qualitative metrics, and custom metrics

 Our samples cover the following tools for evaluation of AI models in Azure:  

| Sample name                            | adversarial | simulator | conversation starter | index | raw text | against model endpoint | against app | qualitative metrics | custom metrics | quantitative NLP metrics |
|----------------------------------------|-------------|-----------|---------------------|-------|----------|-----------------------|-------------|---------------------|----------------|----------------------|
| simulate_adversarial.ipynb            | X           | X         |                     |      |          | X                      |             |                     |                |                      |
| simulate_conversation_starter.ipynb   |             | X         | X                   |       |         | X                      |             |                     |                |                      |
| simulate_input_index.ipynb            |             | X         |                     | X     |          | X                      |             |                     |                |                      |
| simulate_input_text.ipynb             |             | X         |                     |       | X        | X                     |             |                     |                |                      |
| evaluate_endpoints.ipynb              |             |           |                     |      |          | X                      |            | X                    |                |                      |
| evaluate_app.ipynb                    |             |           |                     |       |         |                       | X           | X                    |                |                      |
| evaluate_qualitative.ipynb            |             |           |                     |       |         | X                      |            | X                    |                |                      |
| evaluate_custom.ipynb                 |             |           |                     |       |         | X                      |            |                     | X               |                      |
| evaluate_quantitative.ipynb            |             |           |                     |       |         | X                      |             |                     |               | X                     |
| evaluate_safety_risk.ipynb            | X           |           |                     |       |          | X                     |             |                     |                |                      |
| simulate_and_evaluate_endpoint.py      |             | X         |                     |      | X        | X                     |             | X                    |                |                    |



### Pre-requisites
To use the `azure-ai-evaluation` SDK, install with```pythonpip install azure-ai-evaluation```Python 3.8 or later is required to use this package.- See our Python reference documentation for our `azure-ai-evaluation` SDK[here](https://aka.ms/azureaieval-python-ref) for more granular details oninput/output requirements and usage instructions.- Check out our Github repo for `azure-ai-evaluation` SDK [here](    https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation). 


### Programming Languages
 - Python

### Estimated Runtime: 30 mins
