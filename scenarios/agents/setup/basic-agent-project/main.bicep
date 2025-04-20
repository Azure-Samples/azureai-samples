param ai_services string = 'aiServices'
param project string = 'project'
param projectDescription string = 'some description'
param displayName string = 'project_display_name'
param location string = 'westus2'

param modelName string = 'gpt-4o'
param modelFormat string = 'OpenAI'
param modelVersion string = '2024-11-20'
param modelSkuName string = 'GlobalStandard'
param modelCapacity int = 50

// Create a short, unique suffix, that will be unique to each resource group
// var uniqueSuffix = substring(uniqueString(resourceGroup().id), 0, 4)
param deploymentTimestamp string = utcNow('yyyyMMddHHmmss')
var uniqueSuffix = substring(uniqueString('${resourceGroup().id}-${deploymentTimestamp}'), 0, 4)
var account_name = toLower('${ai_services}${uniqueSuffix}')
var project_name = toLower('${project}${uniqueSuffix}')
/*
  Step 1: Create a Cognitive Services Account and deployment an agent compatible model
  
  - Note: Only public networking is supported.
  
*/ 
module aiAccount 'modules/ai-account-keys.bicep' = {
  name: 'ai-${account_name}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    account_name: account_name
    location: location

    modelName: modelName
    modelFormat: modelFormat
    modelVersion: modelVersion
    modelSkuName: modelSkuName
    modelCapacity: modelCapacity
  }
}

/*
  Step 2: Create a Cognitive Services Project
  
  - Note: Only public networking is supported.
  
*/
module aiProject 'modules/ai-project-keys.bicep' = {
  name: 'ai-${project_name}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    project_name: project_name
    projectDescription: projectDescription
    displayName: displayName
    location: location

    // dependent resources
    account_name: aiAccount.outputs.account_name
  }
}

output ENDPOINT string = aiAccount.outputs.aiServicesTarget
