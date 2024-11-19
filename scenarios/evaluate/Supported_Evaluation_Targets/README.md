---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluate.
---

## Evaluation Target

Evaluation plays a critical role at three pivotal stages:  

* Base Model Evaluation for Model Selection: Initial assessments to identify the most promising base models. 

* Pre-Production AI Application Evaluation: Comprehensive testing to ensure models perform reliably before deployment. 

* Post-Production AI Application Evaluation (Monitoring): Continuous monitoring to maintain performance and adapt to new challenges. 


### Base Model Evaluation for Model Selection 

The first stage of the AI lifecycle involves selecting an appropriate base model. With over 1,600 base models available in the Azure AI Studio's model catalog, it's crucial to choose one that best aligns with your specific use case. This involves comparing models based on quality and safety metrics like groundedness, relevance, and safety scores, as well as considering cost, computational efficiency, and latency. 

Follow [this tutorial](Evaluate_Base_Model_Endpoint/Evaluate_Base_Model_Endpoint.ipynb) to evaluate and compare base models on your own data.

### Pre-Production AI Application Evaluation 

Once a base model is selected, the next stage is building an AI application around it—such as an AI-powered copilot, a retrieval-augmented generation (RAG) system, an agentic AI system, or any other generative AI-based tool. Before deploying the AI application into a production environment, rigorous testing is essential to ensure the model is truly ready for real-world use.  

Follow [this tutorial](Evaluate_App_Endpoint/Evaluate_App_Endpoint.ipynb) to evaluate any AI application endpoint on your own data.

### Post-Production AI Application Evaluation (Monitoring) 

Once the AI application is approved for production and deployed, it’s crucial to ensure it continues to perform safely and generate high-quality responses while maintaining satisfactory performance. 

Learn how you can [use Azure AI to monitor](aka.ms/azureaimonitoring) your AI Applications post production.

