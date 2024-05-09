# Use Azure OpenAI On Your Data With openai-node Library

## Objective

The main objective of this tutorial is to help users understand the process of chatting on top of your own data. By the end of this tutorial, you should be able to:

 - Connect to Azure using AzureOpenAI client
 - Get chat response with your own data

## Time

You should expect to spend 5-10 minutes running this sample. 

## Before you begin

### Set Environment Variables

To start with let us create a config `.env` file with your project details. This file can be used in this sample or other samples to connect to your workspace. A sample `.env` file is provided below with the variables that you need.

```js
OPENAI_API_VERSION="Insert the targeted API version here"
AZURE_OPENAI_ENDPOINT="Insert your endpoint here"
AZURE_OPENAI_API_KEY="Insert your API Key here"
```

### Connect To Your Data Sources
We need to connect to a data source to upload our data. We will set up your own designated data sources using Azure AI Search. 

```js
const dataSources = {
    data_sources: [
        {
            type: "azure_search",
            parameters: {
                endpoint: azureSearchEndpoint,
                index_name: azureSearchIndexName,
                authentication: {
                    type: "api_key",
                    key: azureSearchAdminKey,
                }
            }
        }
    ]
}
```

### Using Azure OpenAI client
We will access Azure Open AI service through `openai-node` library. 

#### Authenticate Using Microsoft Entra ID
```js
const { AzureOpenAI } = require("openai");  
const { getBearerTokenProvider, DefaultAzureCredential } = require("@azure/identity");  

const credential = new DefaultAzureCredential();      
const scope = "https://cognitiveservices.azure.com/.default";

const client = new AzureOpenAI({
    azureADTokenProvider: getBearerTokenProvider(credential, scope),
});
```

## Run AI Models On Your Data

Now we can use Azure on your own data with Chat Completions. Providing our search endpoint, key, and index name in the `data_sources` options, any questions posed to the model will now be grounded in our own data. An additional property, `context`, will be provided in the response to show the data the model referenced to answer the question.

```js
async function main() {
    console.log('== Get chat completions on your own data ==');
    const deploymentName = "gpt-4";
    const result = await client.chat.completions.create({
        model: deploymentName, 
        messages: [{ role: 'user', content: 'Write a poem to celebrate my birthday!' }],
        ...dataSources
    });
    console.log("The content received:", result.choices[0].message?.content);
    console.log("Citations:", result.choices[0].message?.context?.citations);
    console.log("Intent:", result.choices[0].message?.context?.intent);
}

main().catch((err) => {
    console.error(err);
});
```

If you would prefer to stream the response from the model, you can pass the `stream: true` keyword argument:

```js
async function main() {
    console.log('== Stream chat completions on your own data ==');
    const deploymentName = "gpt-4";
    const result = await client.chat.completions.create({
        stream: true,
        model: deploymentName,
        messages: [{ role: 'user', content: 'Write a poem to celebrate my birthday!' }],
        ...dataSources as any
    });

    console.log("The content received:", result.choices[0].message?.content);
    for (const choice of chunk.choices) {
        console.log(choice.delta?.content);
        console.log((choice.delta as any).context?.citations);
        console.log((choice.delta as any).context?.intent);
    }
}

main().catch((err) => {
    console.error(err);
});
```

## Cleaning up

To clean up all Azure resources used in this example, you can delete the individual resources you created in this tutorial.

If you made a resource group specifically to run this example, you could instead [delete the resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group).
