## Azure Functions
Azure Functions are a serverless compute service that lets you run event-triggered code without having to explicitly provision or manage infrastructure. This section provides an example of how to set up an AzureFunction. NOTE: Currently, agents are not included in the sample, but will be added shortly.

Important notes:
The identity of your AI Project MUST be part of the Azure Storage Queue Data Contributor RBAC role for the provisioned storage account. 

Azure Functions intended for use by agents can be deployed anywhere, but they require read/write access to Azure storage queues within the storage account that was provisioned for your AI project. To do that we recommend also adding the identity of your Azure Functions to the Azure Storage Queue Data Contributor RBAC role for the storage account. The identity can be either a system-assigned or user-assigned managed identity. 

 

Known Limitations 

Azure Function support is limited to functions triggered by queue messages. No other triggers are allowed. 

Queue message size is limited by Azure Storage Queues to 64k 

Parallel invocation of multiple Azure Functions from the same agent run is not supported. 

Limit = 128 functions 

FAQ 

Q: How do you integrate a function that is in Azure Functions SDK with Agents SDK? 

A: During the provisioning process, a storage account is created.  

Step 1: connect the Azure Function to this queue that was provisioned for you during hub creation.  

Step 2: when you create an assistant, you create with a payload. Like any other tool, you register the Azure Function, give it a set of functions. Two things are done independently:  

write a function attached to the queue 

issue an assistant request with configuration. These two things are entirely independent (don’t even need to be in the same region), but will talk to each other in the cloud. 

Q: Which Microsoft solution is right for me? 

A: 

Local function calling – Use this option if you’re going to interact with a system device, like opening Spotify (or something on your machine). 

Azure Functions – Use this option if you want to write logic that interacts with other services, that is naturally event-driven or long-running, or if you want to scale. 

Logic Apps – Use this option when you don’t want to write the logic, if you just want to see if there’s an existing connector/tool. E.g., converting a doc to PDF or sending an email. In these examples, the tools already have built-in functions, so there’s no need to create your own. 