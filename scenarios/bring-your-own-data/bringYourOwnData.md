# Use Azure OpenAI On Your Data With openai-node Library

## Objective

Use openai-node Azure client to generate answers from your data using Azure On Your Data feature.

This tutorial uses the following services:

- Access to Azure OpenAI Service - you can apply for access [here](https://go.microsoft.com/fwlink/?linkid=2222006)
- Access to Azure Search Service 

## Time

You should expect to spend 5-10 minutes running this sample. 

## Before you begin

### Set Environment Variables

To start with let us create a config `.env` file with your project details. This file can be used in this sample or other samples to connect to your workspace. 

```ts
// Load the .env file if it exists
import * as dotenv from "dotenv";
dotenv.config();

// You will need to set these environment variables or edit the following values
// The endpoint you will use to access your Azure OpenAI instance
const endpoint = process.env["ENDPOINT"] || "<endpoint>";
// Your Azure OpenAI API key
const azureApiKey = process.env["AZURE_API_KEY"] || "<api key>";
// Your Azure Cognitive Search endpoint, admin key, and index name
const azureSearchEndpoint = process.env["AZURE_SEARCH_ENDPOINT"] || "<search endpoint>";
const azureSearchAdminKey = process.env["AZURE_SEARCH_KEY"] || "<search key>";
const azureSearchIndexName = process.env["AZURE_SEARCH_INDEX"] || "<search index>";
```

### Connect To Your Data Sources
We need to connect to a data source to upload our data. We will set up your own designated data sources using Azure AI Search. 
```ts
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

#### Authenticate Using API Key
```ts
import { AzureOpenAI } from 'openai';

// Make sure to set both AZURE_OPENAI_ENDPOINT with the endpoint of your Azure resource and AZURE_OPENAI_API_KEY with the API key.
// You can find both information in the Azure Portal.
const client = new AzureOpenAI({
    apiKey: azureApiKey,
    apiVersion,
    endpoint,
});
```

#### Authenticate Using Microsoft Entra ID
```ts
import { AzureOpenAI } from 'openai';
import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();      
const scope = "https://cognitiveservices.azure.com/.default";

const client = new AzureOpenAI({
    azureADTokenProvider: getBearerTokenProvider(credential, scope),
    apiVersion,
    endpoint,
});
```

## Run AI Models On Your Data

Now we can use Azure on your own data with Chat Completions. Providing our search endpoint, key, and index name in dataSources, any questions posed to the model will now be grounded in our own data. An additional property, context, will be provided in the response to show the data the model referenced to answer the question.

```ts
async function main() {
    console.log('== Get chat completions on your own data ==');
    const result = await client.chat.completions.create({
        model: "gpt-4",
        messages: [{ role: 'user', content: 'Write a poem to celebrate my birthday!' }],
        ...dataSources as any
    });
    console.log("The content received:", result.choices[0]!.message?.content);
    console.log("Citations:", (result.choices[0]!.message as any).context?.citations);
    console.log("Intent:", (result.choices[0]!.message as any).context?.intent);
}

main().catch((err) => {
    console.error(err);
});
```

If you would prefer to stream the response from the model, you can pass the `stream=true` keyword argument:

```ts
async function main() {
    console.log('== Get chat completions on your own data ==');
    const result = await client.chat.completions.create({
        model: "gpt-4",
        messages: [{ role: 'user', content: 'Write a poem to celebrate my birthday!' }],
        stream: true,
        ...dataSources as any
    });

    for await (const chunk of result) {
        for (const choice of chunk.choices) {
            console.log(choice.delta?.content);
            console.log((choice.delta as any).context?.citations);
            console.log((choice.delta as any).context?.intent);
        }
    }
}

main().catch((err) => {
    console.error(err);
});
```

## Cleaning up

To clean up all Azure resources used in this example, you can delete the individual resources you created in this tutorial.

If you made a resource group specifically to run this example, you could instead [delete the resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group).
