---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluating remotely
---

## Evaluating in the cloud

### Overview

This tutorial provides a step-by-step guide on how to evaluate generative AI or LLMs remotely using a triggered evaluation.

### Objective

The main objective of this tutorial is to help users understand the process of evaluating model remotely in the cloud by triggering an evaluation. This type of evaluation can be used for pre-deployment testing. By the end of this tutorial, you should be able to:

 - Learn about evaluations
 - Evaluate LLM using various evaluators from Azure AI Evaluations SDK remotely in the cloud.

### Note
Remote evaluations do not support `Retrieval-Evaluator`, `ContentSafetyEvaluator`, and `QAEvaluator`. 

#### Region Support for Evaluations

| Region | Hate and Unfairness, Sexual, Violent, Self-Harm, XPIA | Groundedness Pro | Protected Material |
| - | - | - | - |
| UK South | Will be deprecated 12/1/24 | no | no |
| East US 2 | yes | yes | yes |
| Sweden Central | yes | yes | no |
| US North Central | yes | no | no |
| France Central | yes | no | no |
| Switzerland West | yes | no | no |

### Programming Languages
 - Python

### Estimated Runtime: 20 mins