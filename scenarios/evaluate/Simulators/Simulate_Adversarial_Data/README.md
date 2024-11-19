---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Simulator which simulates adversarial questions
---

## Adversarial Simulator

### Overview

This tutorial provides a step-by-step guide on how to use the adversarial simulator

### Objective

The main objective of this tutorial is to help users understand the process of creating and using an adversarial simulator
By the end of this tutorial, you should be able to:
- Use the simulator
- Run the simulator to have an adversarial question answering scenario

### Programming Languages
 - Python

### Basic requirements

To use Azure AI Safety Evaluation for different scenarios(simulation, annotation, etc..), you need an **Azure AI Project.** You should provide Azure AI project to run your safety evaluations or simulations with. First[create an Azure AI hub](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/ai-resources)then [create an Azure AI project](    https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-projects?tabs=ai-studio).You **do not** need to provide your own LLM deployment as the Azure AI Safety Evaluation servicehosts adversarial models for both simulation and evaluation of harmful content andconnects to it via your Azure AI project.Ensure that your Azure AI project is in one of the supported regions for your desiredevaluation metric:

#### Region support for evaluations

| Region | Hate and unfairness, sexual, violent, self-harm, XPIA | Groundedness | Protected material |
| - | - | - | - |
|UK South | Will be deprecated 12/1/24| no | no |
|East US 2 | yes| yes | yes |
|Sweden Central | yes| yes | no|
|US North Central | yes| no | no |
|France Central | yes| no | no |
|SwitzerlandWest| yes | no |no|

For built-in quality and performance metrics, connect your own deployment of LLMs and therefore youcan evaluate in any region your deployment is in.

#### Region support for adversarial simulation
| Region | Adversarial simulation |
| - | - |
|UK South | yes|
|East US 2 | yes|
|Sweden Central | yes|
|US North Central | yes|
|France Central | yes|

### Estimated Runtime: 20 mins