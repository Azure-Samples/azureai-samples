
## Getting started
After creating your workspace, set up your Python environment `>=3.10` and run `az login` to verify your credentials. 

Next, install the azure-ai-evaluation package with evaluate and simulator extras like this:

```
pip install azure-ai-evaluation
```
## Sample descriptions
This samples folder contains python notebooks and scripts which demonstrates the following scenarios:

|scenario|description  |
|--|--|
|`simulate-adversarial-interactions/promptflow-online-endpoint/simulate_and_evaluate_online_endpoint.ipynb` | A Jupyter notebook for simulating an online endpoint and evaluating the result |  
|`simulate-adversarial-interactions/askwiki/simulate_and_evaluate_ask_wiki.ipynb` | A Jupyter notebook for simulating and evaluating a custom application | 
|`simulate-adversarial-interactions/rag/simulate_and_evaluate_rag.ipynb` | A Jupyter notebook for simulating and evaluating a RAG application. |
|`ai-generated-data-query-response/generate-data-query-response.ipynb` | A Jupyter notebook to generate query responses based on text |
|`ai-generated-data-with-conversation-starter/generate-data-with-conversation-starter.ipynb` | A Jupyter notebook to generate a simulated conversation based on pre defined conversation starters |