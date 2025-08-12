---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Evaluate.
---

## Supported Evaluators


Azure AI Evaluation SDK supported a group of evaluators that measure different aspects of a response’s alignment with expectations.  They can be customized, versioned, and shared across an organization, ensuring consistent evaluation metrics and parameters across various projects.  The choice of evaluators will depend on the specific goals of the evaluation, such as assessing quality, safety, or custom requirements tailored to a particular use case. Below are three main categories of evaluators we support via Azure AI SDK and Studio UI: 

Currently, Azure AI Evaluation SDK supports three types of evaluators:  

![Types of Evaluators](./AutomatedEvaluationAzureAIFoundry.jpg)

* [Risk and safety evaluators](AI_Judge_Evaluators_Safety_Risks/): Evaluating potential risks associated with AI-generated content is essential for safeguarding against content risks with varying degrees of severity. This includes evaluating an AI system's predisposition towards generating harmful or inappropriate content. 

* Generation quality evaluators: This involves assessing metrics such as the groundedness, coherence and relevance of generated content using robust [AI-assisted](AI_Judge_Evaluators_Quality/) and [NLP](NLP_Evaluators/) metrics.


* [Custom evaluators](Custom_Evaluators/): Tailored evaluation metrics can be designed to meet specific needs and goals, providing flexibility and precision in assessing unique aspects of AI-generated content. These custom evaluators allow for more detailed and specific analyses, addressing particular concerns or requirements that standard metrics may not cover. 



You can run evaluators locally or [remotely](../Supported_Evaluation_Targets/Evaluate_On_Cloud/Evaluate_On_Cloud.ipynb), log results in the cloud using the evaluation SDK, or integrate them into automated evaluations within the Azure AI Studio UI. 

## Environment Variables
The following environment variables should be set in a `.env` file at the root of the project:

### To run the evaluations:
- `AZURE_OPENAI_ENDPOINT`: The endpoint URL for Azure OpenAI.
- `AZURE_OPENAI_DEPLOYMENT`: The deployment name for the Azure OpenAI model (e.g., `gpt-4o`).
- `MODEL_DEPLOYMENT_NAME`: The deployment name for the model used in evaluations (e.g., `gpt-4o`).
- `AGENT_MODEL_DEPLOYMENT_NAME`: The deployment name for the agent model (e.g., `gpt-4o`).
- `AZURE_OPENAI_API_VERSION`: The API version for Azure OpenAI.
- `AZURE_SUBSCRIPTION_ID`: The Azure subscription ID.
- `PROJECT_NAME`: The name of the Azure project.
- `RESOURCE_GROUP_NAME`: The name of the Azure resource group.
- `AZURE_AI_PROJECT`: The Azure AI project identifier.
- `AZURE_OPENAI_API_KEY`: The API key for Azure OpenAI.

### To upload reports to Azure AI Foundry:
- `REPORT_AZURE_SUBSCRIPTION_ID`: The Azure subscription ID for report uploads.
- `REPORT_PROJECT_NAME`: The project name for report uploads.
- `REPORT_RESOURCE_GROUP_NAME`: The resource group name for report uploads.

Ensure all these variables are properly configured in your `.env` file before running the application.
