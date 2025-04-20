# Azure AI Agent Service: Basic Setup 1RP

## Basic Agent Setup

> **NOTE:** This template required the following workarounds to be performed after it is deployed:
> 
> 1. Create a project connection to your account. This connection is of category: Azure OpenAI and uses authType: ApiKey.
>    
> 2. Assign the project system managed identity (SMI) the following role ‘Azure AI Developer’ on its parent AI Services resource 

This bicep template provisions required resources for a basic project setup. A new Cognitive Services Account is created, a gpt-4o model is deployed, and a new project is created.

All agents created in this project will automatically use Microsoft managed, multitenant search and storage resources.

### Prerequisites
1. Use only allowlisted subscriptions for 1RP. Two known allowlisted subscriptions are:
    * Azure OpenAI - Agents - Experiments - Microsoft Azure
    * AzureAI-Agents-ERA-Corp - Microsoft Azure
    
1. Westus2 is the only region currently enabled for end-to-end testing. Ensure both Cognitive Services Account and Project are created in this region.
   
1. To deploy the template, you must have the following roles:
    * Cognitive Services Contributor or Contributor
    * [This is needed for the workarounds] Owner or Role Based Access Administrator (because we are assigning project SMI the AI Developer Role, won’t be needed once we fix this)
        * Permission for: Microsoft.Authorization/roleAssignments/write 

 
### Steps

1. To deploy this template, click the "Deploy to Azure" button or you can run one of the following commands:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Frefs%2Fheads%2Fmay-2025%2Fscenarios%2Fagents%2Fsetup%2Fbasic-setup%2Fbasic-setup.json)

* Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location westus2
```

* Deploy the template

```bash
    az deployment group create --resource-group <new-rg-name> --template-file basic-setup.bicep
```
