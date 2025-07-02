---
page_type: sample
languages:
- python
products:
- ai-products
- ai-model-inference
- ai-search
- ai-evaluation
description: Hello world samples for the projects SDK client
---

## Project SDK Basic samples

### Overview

This folder contains hello world samples for the projects SDK client. 

### Objective

This is meant to test out code that's used in our [SDK Overview](https://aka.ms/aifoundrysdk) page.

## Create resources

To run this sample, you'll need to create an Azure AI Project with an Azure AI Services resource connected to it. If you have an existing one, you can skip these steps and move to the next section.

### Create an AI Project and AI Services resource

First we'll create a project in Azure AI Studio:
 - Navigate to [ai.azure.com](ai.azure.com)
 - Click **New Project** on the homepage
 - Enter a project name
 - Click **Create new hub**, provide a hub name
 - In **Customize** change the location to **East US 2** or **Sweden Central**
 - Click **Create Project**

This will take about 3 minutes to complete.

### Deploy a gpt-4o-mini model

Now we'll need to deploy a model so that we can call it from code. To start, we'll use a gpt-4o-mini model because it's fast and cheap. You can experiment with using a gpt-4o model for better results.
 - Go to the **Models + Endpoints** page
 - Click the **+ Deploy Model** dropdown and click **Deploy a base model**
 - Select **gpt-4o-mini** from the list and click **Confirm**

Repeat the above steps for text-embedding-ada-002

## Set up a local development environment

First, clone this repo locally from your favorite terminal and open this folder:
```
git clone https://github.com/azure-samples/azureai-samples
cd azureai-samples/scenarios/projects/basic
```

Then run az login to authenticate with Azure:
```
az login
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
source .venv/bin/activate
```

Install the core dependencies to run the sample:
```Python
pip install -r requirements.txt
```

## Configure project string

Go back to the **Overview** page of your project, and in the upper right hand corner click the copy button beside the **Project connection string** field.

Create a ```.env``` file using the sample:
```
cp .env.sample .env
```

Open the ```.env``` file and paste (ctrl-v) the value to the right of the ```AIPROJECT_CONNECTION_STRING=``` variable.

### Try out samples!

Run the different python files to run different code samples in this folder:
```
python <file_name>.py
```

### Estimated Runtime: 10 mins
