---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: 
---

## Image Evaluation

### Overview

This tutorial provides a step-by-step guide on how to evaluate images for safety and quality

### Objective

The main objective of this tutorial is to help users understand the process of evaluating an image for safety and quality
By the end of this tutorial, you should be able to:
- Run an evaluation with the SDK on images for safety and quality

### Programming Languages
 - Python

### Basic requirements

To use Azure AI Safety Evaluation for different scenarios(simulation, annotation, etc..), you need an **Azure AI Project.** You should provide Azure AI project to run your safety evaluations or simulations with. First[create an Azure AI hub](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/ai-resources)then [create an Azure AI project](    https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-projects?tabs=ai-studio).You **do not** need to provide your own LLM deployment as the Azure AI Safety Evaluation servicehosts adversarial models for both simulation and evaluation of harmful content and connects to it via your Azure AI project.

### Estimated Runtime: 15 mins