# Retrieval Augmented Generation (RAG) using Azure AI SDK

This sample shows how to create an index and consume it to answer questions based on your data (aka RAG pattern). It demonstrates how to create an index from local files and folders, how to store that index in Azure Cognitive Search or in [FAISS](https://ai.meta.com/tools/faiss). The index gets created locally and can then be registered to your AI Studio project. Once registered, it can be retrieved and consumed to answer questions. The sample shows how to build a simple QnA script to answer questions.

This sample is useful for developers and data scientists who wish to use their data with LLMs to build QnA bots, co-pilots. Basically anyone interested in using the RAG pattern.