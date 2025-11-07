---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluate RAG systems with Azure AI Evaluation SDK
---


## Evaluate RAG systems with Azure AI Evaluation SDK

### Overview
Best practices for evaluating Retrieval-Augmented Generation (RAG) systems. This tutorial demonstrates how to use the Azure AI Evaluation SDK to evaluate RAG systems, focusing on:
 1) end-to-end RAG evaluation (system response) using [Groundedness](http://aka.ms/groundedness-doc) and [Relevance](http://aka.ms/relevance-doc) evaluators and;
 2) document retrieval quality using [Document Retrieval](https://aka.ms/doc-retrieval-evaluator) evaluator for advanced users who can curate ground truths for retrieval.

To support RAG quality output, it’s important to evaluate the following aspects using RAG triad metrics:
 
•	Retrieval: Is the search output relevant and useful for resolving the user's query? Strong retrieval is critical for providing accurate context. 
•	Groundedness: Is the generated response supported by the retrieved documents (e.g., output of a search tool)? The consistency of the response generated with respect to grounding.
•	Relevance: After agentic retrieval and generation, does  the response fully address the user’s query? This is key to delivering a satisfying experience for the end user.

This tutorial includes two notebooks as best practices to cover these important evaluation aspects:

- [Evaluate and Optimize a RAG retrieval system end to end](https://aka.ms/knowledge-agent-eval-sample): Complex queries are a common scenario for advanced RAG retrieval systems. In both principle and practice, [agentic RAG](aka.ms/agentRAG) is an advanced RAG pattern compared to traditional RAG patterns in agentic scenarios. By using the Agentic Retrieval API in Azure AI Search in Azure AI Foundry, we observe [up to 40% better relevance for complex queries than our baselines](https://techcommunity.microsoft.com/blog/Azure-AI-Services-blog/up-to-40-better-relevance-for-complex-queries-with-new-agentic-retrieval-engine/4413832/). After onboarding to agentic retrieval, it's a best practice to evaluate the end-to-end response of the RAG system with [Groundedness](http://aka.ms/groundedness-doc) and [Relevance](http://aka.ms/relevance-doc) evaluators. With the ability to assess the end-to-end quality for one set of RAG parameter, you can perform "parameter sweep" for another set to finetune and optimize the parameters for the agentic retrieval pipeline.

- [Evaluate and Optimize RAG document retrieval quality](https://aka.ms/doc-retrieval-sample): Document retrieval quality is a common bottleneck in RAG workflows. To address this, one best practice is to optimize your RAG search retrieval parameters according to your enterprise data using golden metrics such as [NDCG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain). This is an advanced scenario where you can curate ground-truth relevance labels for document retrieval results (commonly called qrels) through human subject matter experts or AI-assisted tools such as Github Copilot or using [Relevance](http://aka.ms/relevance-doc) evaluator to label each document. After successful curation of such input data, you can perform "parameter sweep" to finetune and optimize the parameters by evaluating the document retrieval quality using golden metrics and per-document labels for more precise measurements.


### Objective

This tutorial provides a step-by-step guide on how to evaluate RAG systems using quality evaluators. By the end of this tutorial, you should be able to:

 - Learn about evaluators relevant for RAG systems (both end-to-end and document retrieval quality)

### Programming Languages
 - Python

### Estimated Runtime: 30 mins