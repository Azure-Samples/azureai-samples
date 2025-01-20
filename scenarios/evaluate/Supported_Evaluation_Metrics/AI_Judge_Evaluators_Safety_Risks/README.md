---
page_type: sample
languages:
- language1
- language2
products:
- ai-services
- azure-openai
description: Evaluate Risk and Safety of Text - Protected Material and Indirect Attack Jailbreak
---
# Evaluate Risk and Safety of Text - Protected Material and Indirect Attack Jailbreak

## Overview

This notebook walks through how to generate a simulated text conversation targeting a deployed AzureOpenAI model and then evaluate that text conversation dataset for Protected Material and Indirect Attack Jailbreak vulnerability. It also references the prompt filtering capabilities of Azure AI Content Safety Service to help identify and mitigate these vulnerabilities in your AI system.

For a walk through of how to generate a simulated audio conversation targeting a deployed AzureOpenAI audio model and evaluate that conversation for safety risks, see [Azure AI Safety Evaluations of Audio Models](./AI_Judge_Evaluators_Safety_Risks_Audio/AI_Judge_Evaluators_Safety_Risks_Audio.ipynb)

## Objective

The main objective of this tutorial is to help users understand how to use the azure-ai-evaluation SDK to simulate a conversation with an AI system and then evaluate that dataset on various safety metrics. By the end of this tutorial, you should be able to:

- Use azure-ai-evaluation SDK to generate a simulated conversation dataset
- Evaluate the generated dataset for Protected Material and Indirect Attack Jailbreak vulnerability
- Use Azure AI Content Safety filter prompts to mitigate found vulnerabilities

## Basic requirements

To use Azure AI Safety Evaluation for different scenarios(simulation, annotation, etc..), you need an **Azure AI Project.** You should provide Azure AI project to run your safety evaluations or simulations with. First[create an Azure AI hub](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/ai-resources)then [create an Azure AI project](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-projects?tabs=ai-studio).You **do not** need to provide your own LLM deployment as the Azure AI Safety Evaluation servicehosts adversarial models for both simulation and evaluation of harmful content andconnects to it via your Azure AI project.Ensure that your Azure AI project is in one of the supported regions for your desiredevaluation metric:

### Region support for evaluations

| Region | Hate and unfairness, sexual, violent, self-harm, XPIA | Groundedness | Protected material |
| - | - | - | - |
|East US 2 | yes| yes | yes |
|Sweden Central | yes| yes | no|
|US North Central | yes| no | no |
|France Central | yes| no | no |
|Switzerland West| yes | no |no|

For built-in quality and performance metrics, connect your own deployment of LLMs and therefore youcan evaluate in any region your deployment is in.

### Region support for adversarial simulation

| Region | Adversarial simulation |
| - | - |
|UK South | yes|
|East US 2 | yes|
|Sweden Central | yes|
|US North Central | yes|
|France Central | yes|

## Programming Languages

- Python

## Estimated Runtime: 30 mins
