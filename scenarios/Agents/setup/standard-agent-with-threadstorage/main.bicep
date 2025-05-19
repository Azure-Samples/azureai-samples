// Execute this main file to deploy Enterprise Standard Agent setup resources

// Parameters
@minLength(2)
@maxLength(12)
@description('Name for your Azure AI Hub resource.')
param aiHubName string = 'hub-demo'

@description('Friendly name for your Hub resource')
param aiHubFriendlyName string = 'Agents Hub resource'

@description('Creating an Azure AI Hub to set up your app environment and Azure resources.')
param aiHubDescription string = 'This is an example AI Hub resource for use in Azure AI Studio.'

@description('Name for the AI project resources.')
param aiProjectName string = 'project-demo'

@description('Friendly name for your Azure AI resource')
param aiProjectFriendlyName string = 'Agents Project resource'

@description('Creating an Azure AI project under your Hub creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.')
param aiProjectDescription string = 'This is an example AI Project resource for use in Azure AI Studio.'

@description('Azure region used for the deployment of all resources.')
param location string = resourceGroup().location

@description('Set of tags to apply to all resources.')
param tags object = {}

@description('Name of the Azure AI Search account')
param aiSearchName string = 'agent-ai-search'

@description('Name for capabilityHost.')
param capabilityHostName string = 'caphost1'

@description('Name of the storage account')
param storageName string = 'agent-storage'

@description('Name of the Azure AI Services account')
param aiServicesName string = 'agent-ai-services'

@description('Model name for deployment')
param modelName string = 'gpt-4o'

@description('Model format for deployment')
param modelFormat string = 'OpenAI'

@description('Model version for deployment')
param modelVersion string = '2024-08-06'

@description('Model deployment SKU name')
param modelSkuName string = 'GlobalStandard'

@description('Model deployment capacity')
param modelCapacity int = 50

@description('Model deployment location. If you want to deploy an Azure AI resource/model in different location than the rest of the resources created.')
param modelLocation string = 'westus'

@description('AI Service Account kind: either AzureOpenAI or AIServices')
param aiServiceKind string = 'AIServices'

@description('The AI Service Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param aiServiceAccountResourceId string = ''

@description('The Ai Search Service full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param aiSearchServiceResourceId string = ''

@description('The Ai Storage Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param aiStorageAccountResourceId string = ''

@description('The Cosmos DB Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param cosmosDBResourceId string = ''

param cosmosDBName string = 'agent-thread-storage'

// Variables
var name = toLower('${aiHubName}')
var projectName = toLower('${aiProjectName}')

// Create a short, unique suffix, that will be unique to each resource group
// var uniqueSuffix = substring(uniqueString(resourceGroup().id), 0, 4)
param deploymentTimestamp string = utcNow('yyyyMMddHHmmss')
var uniqueSuffix = substring(uniqueString('${resourceGroup().id}-${deploymentTimestamp}'), 0, 4)

module validateExistingResources 'modules-standard/validate-existing-resources.bicep' = {
  name: 'validate-existing-resources-${name}-${uniqueSuffix}-deployment'
  params: {
    aiServiceAccountResourceId: aiServiceAccountResourceId
    aiSearchServiceResourceId: aiSearchServiceResourceId
    aiStorageAccountResourceId: aiStorageAccountResourceId
    cosmosDBResourceId: cosmosDBResourceId
  }
}

// Already validated existing resources. Either create new resources or use existing ones because the resource IDs have been validated
var aiServiceExists = aiServiceAccountResourceId != ''
var acsExists = aiSearchServiceResourceId != ''
var cosmosExists = cosmosDBResourceId != ''

var aiServiceParts = split(aiServiceAccountResourceId, '/')
var aiServiceAccountSubscriptionId = aiServiceExists ? aiServiceParts[2] : subscription().subscriptionId
var aiServiceAccountResourceGroupName = aiServiceExists ? aiServiceParts[4] : resourceGroup().name

var acsParts = split(aiSearchServiceResourceId, '/')
var aiSearchServiceSubscriptionId = acsExists ? acsParts[2] : subscription().subscriptionId
var aiSearchServiceResourceGroupName = acsExists ? acsParts[4] : resourceGroup().name

var cosmosParts = split(cosmosDBResourceId, '/')
var cosmosDBSubscriptionId = cosmosExists ? cosmosParts[2] : subscription().subscriptionId
var cosmosDBResourceGroupName = cosmosExists ? cosmosParts[4] : resourceGroup().name

// Dependent resources for the Azure Machine Learning workspace
module aiDependencies 'modules-standard/standard-dependent-resources.bicep' = {
  name: 'dependencies-${name}-${uniqueSuffix}-deployment'
  params: {
    location: location
    storageName: '${storageName}${uniqueSuffix}'
    keyvaultName: 'kv-${name}-${uniqueSuffix}'
    aiServicesName: '${aiServicesName}${uniqueSuffix}'
    aiSearchName: '${aiSearchName}-${uniqueSuffix}'
    cosmosDBName: '${cosmosDBName}-${uniqueSuffix}'
    tags: tags

     // Model deployment parameters
     modelName: modelName
     modelFormat: modelFormat
     modelVersion: modelVersion
     modelSkuName: modelSkuName
     modelCapacity: modelCapacity
     modelLocation: modelLocation

     // AI Services account parameters
     aiServiceAccountResourceId: aiServiceAccountResourceId
     aiServiceExists: validateExistingResources.outputs.aiServiceExists

     // AI Search Service parameters
     aiSearchServiceResourceId: aiSearchServiceResourceId
     aiSearchExists: validateExistingResources.outputs.aiSearchExists

    // Storage Account
    aiStorageAccountResourceId: aiStorageAccountResourceId
    aiStorageExists: validateExistingResources.outputs.aiStorageExists

    // Cosmos DB Account
     cosmosDBResourceId: cosmosDBResourceId
     cosmosDBExists: validateExistingResources.outputs.cosmosDBExists
    }
}

module aiHub 'modules-standard/standard-ai-hub.bicep' = {
  name: '${name}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    aiHubName: '${name}-${uniqueSuffix}'
    aiHubFriendlyName: aiHubFriendlyName
    aiHubDescription: aiHubDescription
    location: location
    tags: tags


    aiSearchName: aiDependencies.outputs.aiSearchName
    aiSearchId: aiDependencies.outputs.aisearchID
    aiSearchServiceResourceGroupName: aiDependencies.outputs.aiSearchServiceResourceGroupName
    aiSearchServiceSubscriptionId: aiDependencies.outputs.aiSearchServiceSubscriptionId

    aiServicesName: aiDependencies.outputs.aiServicesName
    aiServiceKind: aiServiceKind
    aiServicesId: aiDependencies.outputs.aiservicesID
    aiServicesTarget: aiDependencies.outputs.aiservicesTarget
    aiServiceAccountResourceGroupName:aiDependencies.outputs.aiServiceAccountResourceGroupName
    aiServiceAccountSubscriptionId:aiDependencies.outputs.aiServiceAccountSubscriptionId

    keyVaultId: aiDependencies.outputs.keyvaultId
    storageAccountId: aiDependencies.outputs.storageId
  }
}


module aiProject 'modules-standard/standard-ai-project.bicep' = {
  name: '${projectName}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    aiProjectName: '${projectName}-${uniqueSuffix}'
    aiProjectFriendlyName: aiProjectFriendlyName
    aiProjectDescription: aiProjectDescription
    location: location
    tags: tags
    aiHubId: aiHub.outputs.aiHubID

    cosmosDBName: aiDependencies.outputs.cosmosDBName
    cosmosDBSubscriptionId: aiDependencies.outputs.cosmosDBSubscriptionId
    cosmosDBResourceGroupName: aiDependencies.outputs.cosmosDBResourceGroupName
  }
}

module aiServiceRoleAssignments 'modules-standard/ai-service-role-assignments.bicep' = {
  name: 'ai-service-ra-${projectName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(aiServiceAccountSubscriptionId, aiServiceAccountResourceGroupName)
  params: {
    aiServicesName: aiDependencies.outputs.aiServicesName
    aiProjectPrincipalId: aiProject.outputs.aiProjectPrincipalId
    aiProjectId: aiProject.outputs.aiProjectResourceId
  }
}

module aiSearchRoleAssignments 'modules-standard/ai-search-role-assignments.bicep' = {
  name: 'ai-search-ra-${projectName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(aiSearchServiceSubscriptionId, aiSearchServiceResourceGroupName)
  params: {
    aiSearchName: aiDependencies.outputs.aiSearchName
    aiProjectPrincipalId: aiProject.outputs.aiProjectPrincipalId
    aiProjectId: aiProject.outputs.aiProjectResourceId
  }
}

module cosmosAccountRoleAssignments 'modules-standard/cosmos-account-role-assignments.bicep' = {
  name: 'cosmos-ac-ra-${projectName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(cosmosDBSubscriptionId, cosmosDBResourceGroupName)
  params: {
    cosmosDBName: aiDependencies.outputs.cosmosDBName
    aiProjectPrincipalId: aiProject.outputs.aiProjectPrincipalId
    projectWorkspaceId: aiProject.outputs.aiProjectWorkspaceId

  }
}

module addCapabilityHost 'modules-standard/add-capability-host.bicep' = {
  name: 'capabilityHost-configuration--${uniqueSuffix}-deployment'
  params: {
    capabilityHostName: '${uniqueSuffix}-${capabilityHostName}'
    aiHubName: aiHub.outputs.aiHubName
    aiProjectName: aiProject.outputs.aiProjectName
    acsConnectionName: aiHub.outputs.acsConnectionName
    aoaiConnectionName: aiHub.outputs.aoaiConnectionName
    cosmosConnectionName: aiProject.outputs.cosmosConnectionName
  }
  dependsOn: [
    aiSearchRoleAssignments,aiServiceRoleAssignments, cosmosAccountRoleAssignments
  ]
}


module cosmosContainerRoleAssignments 'modules-standard/cosmos-container-role-assignment.bicep' = {
  name: 'cosmos-ra-${toLower('${projectName}')}-${uniqueSuffix}-deployment'
  scope: resourceGroup(cosmosDBSubscriptionId, cosmosDBResourceGroupName)
  params: {
    cosmosAccountName: aiDependencies.outputs.cosmosDBName
    aiProjectPrincipalId: aiProject.outputs.aiProjectPrincipalId
    aiProjectId: aiProject.outputs.aiProjectResourceId
    projectWorkspaceId: aiProject.outputs.aiProjectWorkspaceId

}
dependsOn: [
  addCapabilityHost
  ]
}

output PROJECT_CONNECTION_STRING string = aiProject.outputs.projectConnectionString
