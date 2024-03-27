---
page_type: sample
languages:
- python
products:
- ai-services
- azure-openai
description: Fine-tuning and inference with function calling samples
---

## Overview

### Fine-tuning with function calling - stock price use case
This repository demonstrates the utility of function calling with fine-tuned models. We want to build an application that retrieves stock prices from an external API, in response to user inquiries. With just the base model, we identified two challenges: (1) the model does a poor job at distinguishing real companies from fake, and (2) our function calling definitions were very long – and increased our tokens per prompt dramatically. We’ll explore how we can use fine tuning, with function calling, to improve the model’s accuracy and performance with the following two use cases:

**Hallucination:** A common problem with large language models is hallucinations – providing plausible but false responses. With function calling, hallucinations can happen when the model calls a function in the wrong context or provides incorrect information to for the function call. We will evaluate whether the fine-tuned model can correctly identify fake companies, and respond appropriately, instead of trying to quote a stock price.

**Token Reduction:** The inclusion of functions in the system message directly impacts token usage. As the number of functions grows, so does the number of tokens within the system message, resulting in verbose prompts and increased costs. Fine tuning lets you shorten your function calls.

We created the train and test datasets for both use cases. Once we create a fine-tuned model that meets our needs, we'll put it all together by developing a basic application that allows users to check stock prices for different companies. We will use YFinance Python library for easy retrieval of current stock prices.

## Objective

We will show you four notebooks as follows:

**fine-tuning-with-function-calling.ipynb** demonstrates how to fine-tune a gpt-35-turbo (0613) model with function calling for our stock price use cases. It also shows how to deploy the fine-tuned model for inference.

**inference-finetuned model-hallucination.ipynb** demonstrates how to do inference with a fine-tuned model to address hallucination use case.

**inference-finetuned model-token reduction.ipynb** illustrates how to do inference with a fine-tuned model for the token reduction use case.

Finally, **finetuning-function calling-e2e application.ipynb** showcases the utilization of a fine-tuned function calling model in an end-to-end application.


## Programing Languages

- Python

## Estimated Runtime: 60-120 mins





 





