# Grounding with Bing Search 

Grounding with Bing Search allows your Azure AI Agents to incorporate real-time public web data when generating responses. To start with, you need to create a Grounding with Bing Search resource, then connect this resource to your Azure AI Agents. When a user sends a query, Azure AI Agents will decide if Grounding with Bing Search should be leveraged or not. If so, it will leverage Bing to search over public web data and return relevant chunks. Lastly, Azure AI Agents will use returned chunks to generate a response.  

Citations show links to websites used to generate response, but don’t show links to the bing query used for the search. Developers and end users don’t have access to raw content returned from Grounding with Bing Search. Grounding with Bing Search is a free service during private preview. 	 

## Setup  

> [!IMPORTANT]
> Grounding with Bing Search has a separate [Terms of Use agreement](https://www.microsoft.com/en-us/bing/apis/grounding-legal-preview) you need to agree to in order to move forward. Please [use this form](https://forms.office.com/r/2j3Sgu8S9K) to sign the agreement. After you have signed the form, it will take 1-3 days for us to whitelist your subscription.

1. Ensure you've completed the prerequisites and setup steps in the [quickstart](../../quickstart.md).

1. Ensure you have loged in to Azure, using `az login`

1. Create a Bing Search resource. If you don’t have one, you can use the Azure CLI to create one 
    
    ```console
    az deployment group create​  
        --name "$deployment_name"​  
        --resource-group "$resource_group"​  
        --template-file "$path_to_arm_template_file"​  
        --parameters "$path_to_parameters_file";​  
    ```
You can find the the template file [here](../bingsearch_arm.json).
An example of the CLI template:
```console
    az deployment group create​  
        --name "az-cli-ARM-TEST"​  
        --resource-group "ApiSearch-Test-WestUS2"​  
        --template-file ".\bingsearch_arm.json"​  
        --parameters ".\bingsearch_arm_params.json";
```

## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've [installed the SDK](../../quickstart.md#install-the-sdk-package) for your language.

* [Python](./python-sample.py)
