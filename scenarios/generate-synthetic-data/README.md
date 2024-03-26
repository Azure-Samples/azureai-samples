
## Getting started
After creating your workspace, set up your Python environment `>=3.10` and run `az login` to verify your credentials. Fill out the `config.json` file with your subscription ID, resource group, and project/workspace name.

Next, install the azure-ai-generative package with evaluate and simulator extras like this:
```
pip install azure_ai_generative[evaluate,simulator]
```

You can install `openai` and `promptflow` with the following versions:
```
pip install openai==1.11.1
pip install promptflow==1.4.1
```
## Sample descriptions
This samples folder contains python scripts which demonstrates the following scenarios:

|scenario|description  |
|--|--|
| `content-generation/simulate_and_evaluate_grounded_content_generator.ipynb` | A Jupyter notebook for simulating and evaluating grounded content generation.
|`adversarial-simulator/content-generation/simulate_and_evaluate_ungrounded_content_generation.ipynb` | A Jupyter notebook for simulating and evaluating ungrounded content generation. | 
|`adversarial-simulator/conversation/simulate_and_evaluate_conversation.ipynb` | A Jupyter notebook for simulating and evaluating conversation. |  
|`adversarial-simulator/qa/simulate_and_evaluate_qa.ipynb` | A Jupyter notebook for simulating and evaluating QA. | 
|`adversarial-simulator/rag/simulate_and_evaluate_rag.py` | A Python script for simulating and evaluating RAG. | 
|`adversarial-simulator/rewrite/simulate_and_evaluate_rewrite.ipynb` | A Jupyter notebook for simulating and evaluating rewrite. | 
|`adversarial-simulator/search/simulate_and_evaluate_search.ipynb` | A Jupyter notebook for simulating and evaluating search. | 
|`adversarial-simulator/summarization/simulate_and_evaluate_summarization.ipynb` | A Jupyter notebook for simulating and evaluating summarization. |  
|`non-adversarial-simulator/conversation/simulate_and_evaluate_conversation.ipynb` | A Jupyter notebook for simulating and evaluating conversation. | 
|`non-adversarial-simulator/summarization/simulate_and_evaluate_summarization.ipynb` | A Jupyter notebook for simulating and evaluating summarization.