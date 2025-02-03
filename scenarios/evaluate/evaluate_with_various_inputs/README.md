---
page_type: sample
languages:
- language1
- language2
products:
- ai-services
- azure-openai
description: Evaluate with various inputs: singleton versus conversation, csv versus jsonl. 
---

## Evaluate With Singletons, Conversations, Jsonl, and Csv

### Overview

This notebook walks through a local toy evaluation using a variety of input types and formats. Many built-in evaluators in the Evaluation SDK can evaluate either a set of single inputs (ex: query and response), or they can derive a list of singleton inputs from a conversation and evaluate those as well.

Additionally, the Evaluation SDK supports reading in datasets from both jsonl files and csv files. This notebook showcases evaluation using both file types.

### Objective

The main objective of this tutorial is to help users understand how to use the azure-ai-evaluation SDK to to evaluate chat data that is stored in any combination of variable type (singleton versus conversation) or file type (jsonl or csv). By the end of this tutorial, you should be able to:

 - Understand how to perform an evaluation using either singleton value or conversations as inputs.
 - Use both jsonl and csv files as inputs for `evaluate`.

### Basic requirements

This notebook is meant to be very lightweight, as such it only requires the Evaluation SDK and the files included in this directory to function.

### Programming Languages
 - Python

### Estimated Runtime: 10 mins