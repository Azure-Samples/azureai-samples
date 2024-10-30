# AI Agents Quick Start 

This QuickStart demonstrates how to quickly set up your first agent with Azure AI Agent Service. 
 
## Complete Azure prerequisites 

1. Create an Azure Subscription for [free](https://azure.microsoft.com/free/ai-services/), if you don't have one already. 

1. Make sure both developers and end users have the following permissions: 

    * `Microsoft.MachineLearningServices/workspaces/agents/read` 
    * `Microsoft.MachineLearningServices/workspaces/agents/action` 
    * `Microsoft.MachineLearningServices/workspaces/agents/delete` 

    If you want to create custom permissions, make sure they have: 

    `agents/*/read` 

    `agents/*/action` 

    `agents/*/delete` 

## Setup your Azure AI Hub and Agent project 

To set up an [Azure AI hub and project](https://learn.microsoft.com/azure/ai-studio/quickstarts/get-started-playground): 

1. Create an Azure AI Hub to set up your app environment and network HOBO resources  

1. Create an Azure AI project under your Hub to provides an endpoint for your app to call, and set up proxy app services to access to resources in your tenant.  

1. Connect an Azure OpenAI resource or an Azure AI resource 

Follow these steps to set up your hub and project: 

1. Install [the Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli-windows?tabs=azure-cli). 

1. Register a provider 
    
    ```console
    az provider register –namespace  {my_resource_namespace} 
    
                         [--accept-terms] 
    
                         [--consent-to-permissions] 
    
                         [--management-group-id] 
    
                         [--wait] 
    ```

1. To authenticate to your Azure subscription from the Azure CLI, use the following command: 

    ```console
    az login
    ```
2. Create a resource group: 

    ```console
    az group create --name {my_resource_group} --location westus2 
    ```

  

Create an Azure OpenAI resource: 

Note: Azure AI Agent Service is currently available for all OpenAI models in available Azure Regions (see the models guide) and Llama 3.1-405B-instruct. We will be expanding to more models in the future. 

  

az cognitiveservices account create --name {my-multi-service-resource} --resource-group {my_resource_group} --kind AIServices --sku s0 --location westus2  

  

       Alternatively, you can create an AI Services resource: 

  

       az cognitiveservices account create --name {MyOpenAIResource} --resource-group {my_resource_group} --location westus2 --kind OpenAI --sku s0  

  

Save the id that gets output, you’ll need it later. It will look similar to: https://eastus.api.cognitive.microsoft.com/  

ai_services_resource_id: /subscriptions/1234-5678-abcd-9fc6-62780b3d3e05/resourceGroups/my-resource-group/providers/Microsoft.CognitiveServices/accounts/multi-service-resource 

  

Create a Bing grounding resource 

az cognitiveservices account create \ 

  --name bing-grounding-resource \ 

  --resource-group <resource-group-name> \ 

  --kind Bing.Grounding \ 

  --sku G1 \ 

  --location Global \ 

  --yes 
 

Create an Azure AI Hub.  
Note: the following command auto creates a storage account, AML workspace and Key Vault 

az ml workspace create --kind hub --resource-group {my_resource_group} --name {my_hub_name} 

 

OR 

 

Optional: If you want to connect an existing storage account and/or key vault you can specify them here: 

az ml workspace create --kind hub --resource-group {my_resource_group} --name {my_hub_name} --location {hub-region} --storage-account {my_storage_account_id} --key-vault {my_key_vault_id} 

 

  

Connect your Hub to your Azure AI resource or Azure OpenAI resource. Replace the resource group and hub name with your resource and hub name. 

Save the following in a file named connection.yml 

If using an AI Services resource, use the following and replace ai_services_resource_id with the fully qualified ID from earlier.   

 

name: myazai_connection  

type: azure_ai_services  

endpoint: https://eastus.api.cognitive.microsoft.com/  

ai_services_resource_id: /subscriptions/12345678-abcd-1234-9fc6-62780b3d3e05/resourceGroups/my-ai-resource-group/providers/Microsoft.CognitiveServices/accounts/multi-service-resource 

If using an Azure OpenAI resource, create the following connection.yml file: 

name: {my_connection_name} 

type: azure_open_ai 

azure_endpoint: https://eastus.api.cognitive.microsoft.com/ 

 

Then run the following command: 

az ml connection create --file connection.yml --resource-group {my_resource_group} --workspace-name {my_hub_name}  

Create a Project.  

Run the following command to find your ARM Template: 

az ml workspace show -n {my_hub_name} --resource-group {my_resource_group} --query id 

Now run this command to create your project 

az ml workspace create --kind project --hub-id {my_hub_ARM_ID} --resource-group {my_resource_group} --name {my_project_name} 