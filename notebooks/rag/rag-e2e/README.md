
## Retrieval Augmented Generation (RAG) using Azure AI SDK

### Overview

This notebook shows how to create an index and consume it to answer questions based on your data (aka RAG pattern). It demonstrates how to create an index from local files and folders, how to store that index in Azure Cognitive Search or in FAISS. The index gets created locally and can then be registered to your AI Studio project. Once registered, it can be retrieved and consumed to answer questions. The sample shows how to build a simple QnA script to answer questions.

This sample is useful for developers and data scientists who wish to use their data with LLMs to build QnA bots, co-pilots. Basically anyone interested in using the RAG pattern.

### Objective

The main objective of this tutorial is to help users understand the process of creating and index, registering the index in the cloud, using that index to build a Q&A bot to answer questions based on the indexed data. By the end of this tutorial, you should be able to:

- Create an index on Azure Cognitive search or FAISS from your local files
- Use the index in a chatbot built using Azure OpenAI and Langchain

### Programming Languages
 - Python
### Estimated Runtime: 20 mins