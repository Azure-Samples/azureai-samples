---
description: This set of templates demonstrates how to set up Azure AI Agent Service with the standard setup, meaning with managed identity authentication for project/hub connections and public internet access enabled. Agents use customer-owned, single-tenant search, file storage, and thread storage resources. With this setup, you have full control and visibility over these resources, but you will incur costs based on your usage.
page_type: sample
products:
- azure
- azure-resource-manager
urlFragment: standard-agent
languages:
- bicep
- json
---
# Standard Agent Setup with thread storage 

> [!IMPORTANT]
> This is the complete Standard Agent Setup with Bring Your Own (BYO) Thread Storage. With this setup, all customer data stored by Agent Service will remain in your own resources, ensuring you have full control over your data.

![Azure Public Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/PublicLastTestDate.svg)
![Azure Public Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/PublicDeployment.svg)

![Azure US Gov Last Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/FairfaxLastTestDate.svg)
![Azure US Gov Last Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/FairfaxDeployment.svg)

![Best Practice Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/BestPracticeResult.svg)
![Cred Scan Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/CredScanResult.svg)

![Bicep Version](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/standard-agent/BicepVersion.svg)

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fstandard-agent-with-threadstorage%2Fazuredeploy.json)

[![Visualize](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/visualizebutton.svg?sanitize=true)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fstandard-agent%2Fazuredeploy.json)

## Overview 

This template demonstrates how to configure Standard Agent Setup with support for the **new feature BYO thread storage with Azure Cosmos DB.**

Resources for the hub, project, storage account, key vault, AI Services, Azure AI Search, and Cosmos DB Account will be automatically created for you. The AI Services, AI Search, Cosmos DB Account, and Azure Storage Account will be connected to your project/hub using managed identity for authentication and a gpt-4o model will be deployed in the eastus region.

## Customization
You can optionally use existing resources for AI Services, AI Search, Cosmos DB, and Azure Blob Storage. Update the following parameters in the parameters file to provide the full ARM resource ID of the existing resources:

- `aiServiceAccountResourceId`
- `aiSearchServiceResourceId`
- `aiStorageAccountResourceId`
- `cosmosDBResourceId`

If you want to use an **existing Azure OpenAI resource**, you will need to update the `aiServiceAccountResourceId` and the `aiServiceKind` parameter in the parameters file. Set the `aiServiceKind` parameter to `AzureOpenAI`.

## Resources

| Provider and type | Description |
| - | - |
| `Microsoft.Resources/resourceGroups` | The resource group all resources get deployed into |
| `Microsoft.KeyVault/vaults` | An Azure Key Vault instance associated to the Azure Machine Learning workspace |
| `Microsoft.Storage/storageAccounts` | An Azure Storage instance associated to the Azure Machine Learning workspace |
| `Microsoft.MachineLearningServices/workspaces` | An Azure AI hub (Azure Machine Learning RP workspace of kind 'hub') |
| `Microsoft.MachineLearningServices/workspaces` | An Azure AI project (Azure Machine Learning RP workspace of kind 'project') |
| `Microsoft.CognitiveServices/accounts` | An Azure AI Services as the model-as-a-service endpoint provider (allowed kinds: 'AIServices' and 'OpenAI') |
| `Microsoft.CognitiveServices/accounts/deployments` | A gpt-4o model is deployed |
| `Microsoft.Search/searchServices` | An Azure AI Search account  |
| `Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview` | An Azure Cosmos DB Account |
