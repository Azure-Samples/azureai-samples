---
page_type: sample

languages: 
  - Python

products: 
  - ai-services
  - azure-openai

description: Azure AI Agents Service supports function calling, which allows you to describe the structure of functions to an Agent and then return the functions that need to be called along with their arguments.
---

# Function Calling 




## Setup

To use function calling, you need a function defined that can be called by the AI Agent service. You can find an example in the [user_functions.py](./user_functions.py) file in this folder. 

## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've [installed the SDK](../README.md#install-the-sdk-package) for your language.

* [Python - function calling](./python-function-calling.py)
* [Python - function calling with automatic tool calling](./python-function-calling-toolset.py)
* [Python - function calling with streaming](./python-function-calling-streaming.py)

## Additional samples

Get the latest stock price using function calling with Yfinance ([shown in Personal Finance Assistant](https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/Assistants/api-in-a-box/personal_finance/assistant-personal_finance.ipynb))
