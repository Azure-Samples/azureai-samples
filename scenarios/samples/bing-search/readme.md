# Grounding with Bing Search 

Grounding with Bing Search allows your Azure AI Agents to incorporate real-time public web data when generating responses. To start with, you need to create a Grounding with Bing Search resource, then connect this resource to your Azure AI Agents. When a user sends a query, Azure AI Agents will decide if Grounding with Bing Search should be leveraged or not. If so, it will leverage Bing to search over public web data and return relevant chunks. Lastly, Azure AI Agents will use returned chunks to generate a response.  

Citations show links to websites used to generate response, but don’t show links to the bing query used for the search. Developers and end users don’t have access to raw content returned from Grounding with Bing Search. 

You can ask questions such as "what is the weather in Seattle?" "what is the recent update in ratail industry in the US?" that require real-time public data.

> [!IMPORTANT]
Grounding with Bing Search is a free service during private preview and your usage will start incurring cost since the integration with Azure AI Agent Service releases to public preview.	 

## Setup  

> [!IMPORTANT]
> 1. Grounding with Bing Search has a separate [Terms of Use agreement](https://www.microsoft.com/en-us/bing/apis/grounding-legal-preview) you need to agree to in order to move forward. Please [use this form](https://forms.office.com/r/2j3Sgu8S9K) to sign the agreement. After you have signed the form, it will take 1-3 days for us to whitelist your subscription.
> 2. Please make sure your resource is created in `EastUS`.
> 3. We recommend using the following models: `gpt-3.5-turbo-0125`, `gpt-4-0125-preview`, `gpt-4-turbo-preview`, `gpt-4-turbo`, `gpt-4-turbo-2024-04-09`, `gpt-4o`, `gpt-4o-mini`, `gpt-4o-mini-2024-07-18`

1. Ensure you've completed the prerequisites and setup steps in the [quickstart](../../quickstart.md).

1. Ensure you have loged in to Azure, using `az login`

1. Register the Bing Search provider
   ```console
       az provider register --namespace 'Microsoft.Bing'
   ```

1. Create a new Grounding with Bing Search resource. You can find the the template file [here](./bingsearch_arm.json) and parameter file [here](./bingsearch_para.json). Make sure you have replace "BING_RESOURCE_NAME" in the parameter file. You can use Azure CLI command: 
    
    ```console
    az deployment group create​  
        --name "$deployment_name"​  
        --resource-group "$resource_group"​  
        --template-file "$path_to_arm_template_file"​  
        --parameters "$path_to_parameters_file";​  
    ```
    An example of the CLI command:
   ```console
       az deployment group create​  
        --name az-cli-ARM-TEST 
        --resource-group ApiSearch-Test-WestUS2
        --template-file bingsearch_arm.json
        --parameters bingsearch_para.json
    ```
   Make sure you have created this Grounding with Bing Search resource in the same resource group of your Azure AI Agent, AI Project, etc.
1. After you have created a Grounding with Bing Search resource, you can find it in [Azure Portal](https://ms.portal.azure.com/#home). Going to the resource group you have created the resource at, search for the Grounding with Bing Search resource you have created.
![image](https://github.com/user-attachments/assets/3b22c48d-987c-4234-a9eb-67aefe3af81c)
1. Click the Grounding with Bing Search resource you have created and copy any of the API key
![image](https://github.com/user-attachments/assets/be98e07d-c91d-4ff9-a97c-6f02c3265221)
1. Go to [Azure AI Studio](https://ai.azure.com/) and select the AI Project(make sure it's in the same resource group of your Grounding with Bing Search resource). Click Settings and then "+new connection" button in Settings page
![image](https://github.com/user-attachments/assets/28bfebda-f3a4-4638-b714-a128a8fa48cb)
![image](https://github.com/user-attachments/assets/7bb9c98e-dd46-4031-be9d-17c70613f222)
1. Select "API key" custom connection in other resource types
![image](https://github.com/user-attachments/assets/7577c912-cf0f-433a-910b-3d9e0ad138c4)
1. Enter the following information and then create a new connection to your Grounding with Bing Search resource
- Endpoint: https://api.bing.microsoft.com/
- Key: YOUR_API_KEY
- Connection name: YOUR_CONNECTION_NAME (You will use this connection name in the sample code below.)
- Access: you can choose either "this project only" or "shared to all projects". Just make sure in the sample code below, the project you entered connection string for has access to this connection.


## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've [installed the SDK](../../quickstart.md#install-the-sdk-package) for your language.

* [Python](./bing-python.py)
* [C#](./BingSearch.cs)
