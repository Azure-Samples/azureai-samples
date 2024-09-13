---
page_type: sample
languages:
- language1
- language2
products:
- ai-services
- azure-openai
description: Evaluate Protected Material and Indirect Attack Jailbreak
---

## Evaluate Protected Material and Indirect Attack Jailbreak

### Overview

This notebook walks through how to generate a simulated conversation targeting a deployed AzureOpenAI model and then evaluate that conversation dataset for Protected Material and Indirect Attack Jailbreak vulnerability. It also references the prompt filtering capabilities of Azure AI to help identify and mitigate these vulnerabilities in your AI system.

### Objective

The main objective of this tutorial is to help users understand how to use the promptflow-evals package to simulate a conversation with an AI system and then evaluate that dataset on various safety metrics. By the end of this tutorial, you should be able to:

 - Use promptflow-evals to generate a simulated conversation dataset
 - Evaluate the generated dataset for Protected Material and Indirect Attack Jailbreak vulnerability
 - Use Azure AI to filter prompts to mitigate found vulnerabilities

### Programming Languages
 - Python

### Estimated Runtime: 30 mins