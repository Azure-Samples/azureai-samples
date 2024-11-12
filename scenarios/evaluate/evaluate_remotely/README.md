---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluating remotely
---

## Evaluating qualitative metrics

### Overview

This tutorial provides a step-by-step guide on how to evaluate LLMs remotely using a triggered evaluation.

### Objective

The main objective of this tutorial is to help users understand the process of evaluating model remotely in the cloud by triggering an evaluation. This type of evaluation can be used for pre-deployment testing. By the end of this tutorial, you should be able to:

 - Learn about evaluations
 - Evaluate LLM using various evaluators from Azure AI Evaluations SDK remotely in the cloud.

### Note
Remote evaluations do not support `Groundedness-Pro-Evaluator`, `Retrieval-Evaluator`, `Protected-Material-Evaluator`, `Indirect-Attack-Evaluator`, `ContentSafetyEvaluator`, and `QAEvaluator`. 

### Programming Languages
 - Python

### Estimated Runtime: 20 mins