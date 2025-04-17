---
page_type: sample
languages:
- language1
- language2
products:
- ai-services
- azure-openai
description: Evaluate with various inputs: query/response versus conversation, csv versus jsonl. 
---

## Evaluate With Queries and Responses, Conversations, Jsonl, and Csv

### Overview

This notebook walks through a local toy evaluation using a variety of input types and formats. Many built-in evaluators in the Evaluation SDK can evaluate either a set on inputs like a query and response, or they can derive a list of query/response pairs from a conversation and evaluate those as well.

Additionally, the Evaluation SDK supports reading in datasets from both jsonl files and csv files. This notebook showcases evaluation using both file types.

### Objective

The main objective of this tutorial is to help users understand how to use the azure-ai-evaluation SDK to to evaluate chat data that is stored in any valid combination of variable type (query/response versus conversation) or file type (jsonl or csv). By the end of this tutorial, you should be able to:

 - Understand how to perform an evaluation using either query/response values or conversations as inputs.
 - Use both jsonl and csv files as inputs for `evaluate`.

### Basic requirements

This notebook is meant to be very lightweight, as such it only requires the Evaluation SDK and the files included in this directory to function.

### Programming Languages
 - Python

### Estimated Runtime: 10 mins