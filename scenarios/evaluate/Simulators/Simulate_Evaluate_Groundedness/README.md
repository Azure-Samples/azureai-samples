---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Simulator and evaluator for assessing groundedness in custom applications using adversarial questions
---

## Simulator and Evaluator for Groundedness (simulate_evaluate_groundedness.ipynb)

### Overview

This tutorial provides a step-by-step guide on how to use the simulator and evaluator to assess the groundedness of responses in a custom application.

### Objective

The main objective of this tutorial is to help users understand the process of creating and using a simulator and evaluator to test the groundedness of responses in a custom application. By the end of this tutorial, you should be able to:
- Use the simulator to generate adversarial questions
- Run the evaluator to assess the groundedness of the responses

### Programming Languages
- Python

### Basic Requirements

To use Azure AI Safety Evaluation for different scenarios (simulation, annotation, etc.), you need an **Azure AI Project.** You should provide an Azure AI project to run your safety evaluations or simulations with. First, [create an Azure AI hub](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/ai-resources) then [create an Azure AI project](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-projects?tabs=ai-studio). You **do not** need to provide your own LLM deployment as the Azure AI Safety Evaluation service hosts adversarial models for both simulation and evaluation of harmful content and connects to it via your Azure AI project. Ensure that your Azure AI project is in one of the supported regions for your desired evaluation metric:

#### Region Support for Evaluations

| Region | Hate and Unfairness, Sexual, Violent, Self-Harm, XPIA | Groundedness | Protected Material |
| - | - | - | - |
| UK South | Will be deprecated 12/1/24 | no | no |
| East US 2 | yes | yes | yes |
| Sweden Central | yes | yes | no |
| US North Central | yes | no | no |
| France Central | yes | no | no |
| Switzerland West | yes | no | no |

For built-in quality and performance metrics, connect your own deployment of LLMs and therefore you can evaluate in any region your deployment is in.

#### Region Support for Adversarial Simulation

| Region | Adversarial Simulation |
| - | - |
| UK South | yes |
| East US 2 | yes |
| Sweden Central | yes |
| US North Central | yes |
| France Central | yes |

### Estimated Runtime: 20 mins