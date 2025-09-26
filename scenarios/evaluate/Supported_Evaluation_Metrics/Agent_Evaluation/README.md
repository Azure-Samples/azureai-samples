---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluate AI agents with Azure AI Evaluation SDK
---


## Evaluate AI agents with Azure AI Evaluation SDK

### Overview

A general AI agent workflow typically contains a linear workflow of intent resolution, tool calling, and final response, at a minimum. We abstracted these evaluation aspects to enable observability user for users into an agent system. You can seamlessly evaluate AI agents using Azure AI Agent Service via converter support. You can also follow the input schema of each evaluator to use our evaluator, detailed in each notebook. We enable evaluation support for AI agents on these aspects:
- [Intent resolution](https://aka.ms/intentresolution-sample): measures the extent of which an agent identifies the correct intent from a user query. 
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample): evaluates the agent’s ability to select the appropriate tools, and process correct parameters from previous steps.
- [Task adherence](https://aka.ms/taskadherence-sample): measures the extent of which an agent’s final response adheres to the task based on its system message and a user query.
- [Response Completeness](https://aka.ms/rescompleteness-sample): measures the extent of which an agent or RAG response is complete (does not miss critical information) compared to the ground truth.
- [End-to-end Azure AI agent evaluation](https://aka.ms/e2e-agent-eval-sample): create an agent using Azure AI Agent Service and seamlessly evaluate its thread and run data, via converter support.
- [End-to-end SK Chat Completion Agent evaluation](Evaluate_SK_Chat_Completion_Agent.ipynb): create an SK Chat Completion Agent and evaluate its thread and run data, via converter support.
### Objective

This tutorial provides a step-by-step guide on how to evaluate AI agents using quality evaluators. By the end of this tutorial, you should be able to:

 - Learn about evaluators relevant for AI agents
 - Evaluate Azure AI agents and other agents using these evaluators   

### Programming Languages
 - Python

### Estimated Runtime: 15 mins