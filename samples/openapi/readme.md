# Use OpenAPI 3.0 Specified Tools 

The Custom Tools feature allows developers to describe custom tools in the Agent API using an [OpenAPI schema](https://www.openapis.org/), enabling the model to intelligently call these functions based on user input. You can use any API spec that is written according to the OpenAPI 3.0 schema. 

While you can use [function calling](../function-calling/readme.md) to define functions you want your agent to call, the OpenAPI tool described here gives you:

* Standardization by letting you leverage the OpenAPI spec when defining your tools 
* Server-side integration with the ability to use managed identity

## Setup 

You need a function defined using the OpenAPI Schema. See the [example function](./function-example.json) for a full sample of a possible tool definition. It will look something like this:  

```yml
openapi: 3.0.1  
info:  
  title: Weather Service API  
  description: This is a sample API for retrieving weather information.  
  version: 1.0.0  
servers:  
  - url: https://api.example.com/weather  
    description: Main API Server  
paths:  
  /current:  
    get:  
      summary: Get current weather  
      operationId: getCurrentWeather 
... 
```


Authentication can be either `anonymous` (no authentication) or `managed_identity`: 

`"auth": { "type": "managed_identity", "security_scheme": { "audience": "https://cognitiveservices.azure.com/" }}` 

`Anonymous` is not authentication, `managed_identity` is authenticating with various Azure Services using RBAC.  

## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've [installed the SDK](../../quickstart.md#install-the-sdk-package) for your language.

* [Python](./python-sample.py)
 
