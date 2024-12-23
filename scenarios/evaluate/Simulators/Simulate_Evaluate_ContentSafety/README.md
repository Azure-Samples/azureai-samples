---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Simulate and Evaluate Content Safety Harms
---

# Simulate and Evaluate Content Safety Harms

## Overview

This notebook walks through how to generate a multi-turn simulated conversation targeting a deployed AzureOpenAI model and then evaluate that conversation dataset for Content Safety harms. 

### Objective

The main objective of this tutorial is to help users understand how to use the azure-ai-evaluation SDK to simulate a multi-turn conversation with an AI system and then evaluate that dataset on various safety metrics. By the end of this tutorial, you should be able to:

- Use azure-ai-evaluation SDK to generate a multi-turn simulated conversation dataset
- Evaluate the generated dataset for Content Safety harms

### Basic requirements

To use Azure AI Safety Evaluation for different scenarios(simulation, annotation, etc..), you need an **Azure AI Project.** You should provide Azure AI project to run your safety evaluations or simulations with. First[create an Azure AI hub](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/ai-resources)then [create an Azure AI project](    https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-projects?tabs=ai-studio).You **do not** need to provide your own LLM deployment as the Azure AI Safety Evaluation servicehosts adversarial models for both simulation and evaluation of harmful content and connects to it via your Azure AI project. Ensure that your Azure AI project is in one of the supported regions for your desiredevaluation metric

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

### Programming Languages

- Python

### Estimated Runtime: 30 mins