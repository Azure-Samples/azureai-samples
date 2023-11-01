# Retrieval Augmented Generation (RAG)

The notebooks in this folder provide examples of how to implement Retrieval Augmented Generation (RAG), a pattern used in AI which uses an LLM to generate answers with your own data.

These samples are useful for developers and data scientists who wish to use their data with LLMs to build QnA bots, co-pilots. It covers how to create indexes and how to consume those indexes.

|Notebook|Description|
|--|--|
|[RAG using Azure AI SDK](rag-qna.ipynb)|This notebook demonstrates how to create an index and consume it to answer questions based on your data (aka RAG pattern). It demonstrates how to create an index and build a simple QnA script to answer questions from that index.|
|[Create index from various sources](create-index-from-various-sources.ipynb)|This notebook demonstrates how to create an index from different sources like local files and remote sources like a git repo and cloud storage URLs.|
