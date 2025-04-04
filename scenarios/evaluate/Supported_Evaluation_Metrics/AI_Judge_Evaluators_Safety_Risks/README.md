---
page_type: sample
languages:
- language1
- language2
products:
- ai-services
- azure-openai
description: Evaluate Risk and Safety of Text/Image/Audio.
---
# Evaluate Risk and Safety of GenAI models and applications: Text, Image and Audio.

## Overview

These notebooks walks through how to evaluate text, image generation/understanding or audio conversation datasets for safety risks evaluations. 

## Objective

The main objective of this tutorial is to help users understand how to use the azure-ai-evaluation SDK to evaluate variety of datasets on various safety metrics. By the end of this tutorial, you should be able to:

- Evaluate text conversations for
  - Content safety (Hateful and unfair, Violent, Sexual and Self-harm-related content)
  - Protected material
  - Direct Attack Jailbreak vulnerability
  - Indirect Attack Jailbreak vulnerability
  - Code vulnerability
  - Ungrounded attributes
- Evaluate image and multi-modal image/text datasets for Content safety
- Evaluate image and multi-modal image/text datasets for Protected materials
- Evaluate audio conversation datasets for Content safety
- Evaluate images datasets for harmful content.
- Evaluate audio conversation datasets for harmful content.
- Evaluate Ungrounded inference of human attributes.
- Evaluate code vulnerabilities.
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
|East US 2 | yes|
|Sweden Central | yes|
|US North Central | yes|
|France Central | yes|

## Programming Languages

- Python

## Estimated Runtime: 30 mins
