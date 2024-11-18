---
page_type: sample
languages:
- python
products:
- ai-model-inference
- ai-search
- ai-evaluation
description: Custom rag app sample using Azure AI SDKs
---

## Custom RAG App

### Overview

This folder contains a reference implementation of a custom RAG app built using the Azure Foundry AI SDK.

Check out the following files for implementation details:
 - [create_search_index.py](): creates an Azure AI search index 
    - Uses data in [assets/products.csv]() to generate the index
 - [get_product_documents.py](): implements document retreival based on user queries
    - Using [assets/intent_mapping.prompty]() for generating a search query from the conversation
 - [chat_with_products.py](): implements chat that grounds response in retrieved documents
    - Uses [assets/grounded_chat.prompty]() for formatting retrieved documents into the chat prompt
    - Implements the [Microsoft AI Chat protocol](https://github.com/microsoft/ai-chat-protocol) for compatibility with evaluation and front-ends

### Objective

The main objective of this sample is for you to understand how to build a custom knowledge retrieval (RAG) app using the Azure AI Inferencing SDK. We'll be putting together inferencing, tracing, evaluation, prompts and search to build a fully custom rag app!

This tutorial uses the following services:
 - Azure Model inference
 - Azure AI Search
 - Application Insights
 - Azure AI projects

## Create resources

To run this sample, you'll need to create an Azure AI Project with an Azure AI Services resource connected to it. If you have an existing one, you can skip these steps and move to the next section.

### Create an AI Project and AI Services resource

First we'll create a project in Azure AI Studio:
 - Navigate to [ai.azure.com](ai.azure.com)
 - Click **New Project** on the homepage
 - Enter a project name
 - In **Customize** change the location to **East US 2** or **Sweden Central**
 - Click **Create new hub**, provide a hub name
 - Click **Create Project**

This will take about 3 minutes to complete.

### Deploy a gpt-4o-mini model

Now we'll need to deploy a model so that we can call it from code. To start, we'll use a gpt-4o-mini model because it's fast and cheap. You can experiment with using a gpt-4o model for better results.
 - Go to the **Models + Endpoints** page
 - Click the **+ Deploy Model** dropdown and click **Deploy a base model**
 - Select **gpt-4o-mini** from the list and click **Confirm**

Repeat the above steps to add a **text-embedding-ada-002**.

## Set up a local development environment

First, clone this repo locally from your favorite terminal and open this folder:
```
git clone https://github.com/azure-samples/azureai-samples
cd azureai-samples/scenarios/rag/custom-rag-app
```

### Creating a local Python environment

First, create a virtual environment. Always do this when installing packages locally >:(

On Windows:
```
py -3 -m venv .venv
.venv\scripts\activate
```

On Linux:
```
python3 -m venv .venv
source venv/bin/activate
```

Install the full set of dependencies to run the sample:
```Python
pip install -r dev-requirements.txt
```

### Log in to the Azure CLI
If you haven't already, you'll need to log in to the Azure CLI in your terminal. It will open a browser for you to authenticate and then log you in in the terminal.
```Python
az login
```

## Configure project string

Go back to the **Overview** page of your project, and in the upper right hand corner click the copy button beside the **Project connection string** field.

Create a ```.env``` file using the sample:
```
cp .env.sample .env
```

Open the ```.env``` file and paste (ctrl-v) the value to the right of the ```AIPROJECT_CONNECTION_STRING=``` variable.


### Run the sample!

Create a search index:
```
python create_search_index.py
```

Test out what documents are retrieved from the search index by running:
```
python get_product_documents.py --query "I need a new tent for 4 people, what would you recommend?"
```

Run a sample user input through the ```chat_with_products``` function:
```
python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?"
```

#### Tracing

To enable tracing, first install packages needed for logging telemetry to AI Studio projects:
```
pip install azure-monitor-opentelemetry
```

Now run the application with telemetry enabled:
```
python chat_with_products.py --enable-telemetry
```

Click the link at the start of the output to view your traces in Azure AI Studio!

#### Evaluation

Install packages needed to run evaluation (this can take up to 8 minutes):
```
pip install azure-ai-evaluation[remote]
```

Run evaluation:
```
python evaluate.py
```

### Estimated Runtime: 30 mins
