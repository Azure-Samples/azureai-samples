// Standard agent setup 

@description('The region to deploy your AI Services resource and project')
param location string = resourceGroup().location

@description('Name for your AI Services resource.')
param ai_services string = 'aiServices'

@description('Name for your project resource.')
param projectName string = 'project'

@description('This project will be a sub-resource of your account')
param project_description string = 'some description'

@description('The display name of the project')
param display_name string = 'project_display_name'

// Model deployment parameters
@description('The name of the model you want to deploy')
param modelName string = 'gpt-4o'
@description('The provider of your model')
param modelFormat string = 'OpenAI'
@description('The version of your model')
param modelVersion string = '2024-05-13'
@description('The sku of your model deployment')
param modelSkuName string = 'GlobalStandard'
@description('The tokens per minute (TPM) of your model deployment')
param modelCapacity int = 1

@description('The AI Search Service full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param aiSearchResourceId string = ''

@description('The AI Storage Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param azureStorageAccountResourceId string = ''

@description('The Cosmos DB Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param azureCosmosDBAccountResourceId string = ''

param projectCapHost string = 'caphostproj'
param accountCapHost string = 'caphostacc'
// Create a short, unique suffix, that will be unique to each resource group
param deploymentTimestamp string = utcNow('yyyyMMddHHmmss')
var uniqueSuffix = substring(uniqueString('${resourceGroup().id}-${deploymentTimestamp}'), 0, 4)
var account_name = toLower('${ai_services}${uniqueSuffix}')
var project_name = toLower('${projectName}${uniqueSuffix}')


var cosmosDBName = toLower('${ai_services}${uniqueSuffix}cosmosdb')
var aiSearchName = toLower('${ai_services}${uniqueSuffix}search')
var azureStorageName = toLower('${ai_services}${uniqueSuffix}storage')

// Check if existing resources have been passed in
var storagePassedIn = azureStorageAccountResourceId != ''
var searchPassedIn = aiSearchResourceId != ''
var cosmosPassedIn = azureCosmosDBAccountResourceId != ''

var acsParts = split(aiSearchResourceId, '/')
var aiSearchServiceSubscriptionId = searchPassedIn ? acsParts[2] : subscription().subscriptionId
var aiSearchServiceResourceGroupName = searchPassedIn ? acsParts[4] : resourceGroup().name

var cosmosParts = split(azureCosmosDBAccountResourceId, '/')
var cosmosDBSubscriptionId = cosmosPassedIn ? cosmosParts[2] : subscription().subscriptionId
var cosmosDBResourceGroupName = cosmosPassedIn ? cosmosParts[4] : resourceGroup().name

var storageParts = split(azureStorageAccountResourceId, '/')
var azureStorageSubscriptionId = storagePassedIn ? storageParts[2] : subscription().subscriptionId
var azureStorageResourceGroupName = storagePassedIn ? storageParts[4] : resourceGroup().name

// Checks if existing resources have been passed in
module validateExistingResources 'modules-standard/validate-existing-resources.bicep' = {
  name: 'validate-existing-resources-${uniqueSuffix}-deployment'
  params: {
    aiSearchResourceId: aiSearchResourceId
    azureStorageAccountResourceId: azureStorageAccountResourceId
    azureCosmosDBAccountResourceId: azureCosmosDBAccountResourceId
  }
}

// This module will create new agent dependent resources
// A Cosmos DB account, an AI Search Service, and a Storage Account are created if they do not already exist
module aiDependencies 'modules-standard/standard-dependent-resources.bicep' = {
  name: 'dependencies-${account_name}-${uniqueSuffix}-deployment'
  params: {
    location: location
    azureStorageName: azureStorageName
    aiSearchName: aiSearchName
    cosmosDBName: cosmosDBName

    //keyvaultName: 'kv-${name}-${uniqueSuffix}'

    //  // AI Services account parameters
    //  aiServiceAccountResourceId: aiServiceAccountResourceId
    //  aiServiceExists: validateExistingResources.outputs.aiServiceExists
    
    // AI Search Service parameters
    aiSearchResourceId: aiSearchResourceId
    aiSearchExists: validateExistingResources.outputs.aiSearchExists

    // Storage Account
    azureStorageAccountResourceId: azureStorageAccountResourceId
    azureStorageExists: validateExistingResources.outputs.azureStorageExists

    // Cosmos DB Account
    cosmosDBResourceId: azureCosmosDBAccountResourceId
    cosmosDBExists: validateExistingResources.outputs.cosmosDBExists
    }
}

module aiAccount 'modules-standard/ai-account-identity.bicep' = {
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
  dependsOn: [
    validateExistingResources, aiDependencies
  ]
}

module aiProject 'modules-standard/ai-project-identity.bicep' = {
  name: 'ai-${project_name}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    project_name: project_name
    projectDescription: project_description
    display_name: display_name
    location: location

    aiSearchName: aiDependencies.outputs.aiSearchName
    aiSearchServiceResourceGroupName: aiDependencies.outputs.aiSearchServiceResourceGroupName
    aiSearchServiceSubscriptionId: aiDependencies.outputs.aiSearchServiceSubscriptionId

    cosmosDBName: aiDependencies.outputs.cosmosDBName
    cosmosDBSubscriptionId: aiDependencies.outputs.cosmosDBSubscriptionId
    cosmosDBResourceGroupName: aiDependencies.outputs.cosmosDBResourceGroupName

    azureStorageName: aiDependencies.outputs.azureStorageName
    azureStorageSubscriptionId: aiDependencies.outputs.azureStorageSubscriptionId
    azureStorageResourceGroupName: aiDependencies.outputs.azureStorageResourceGroupName
    // dependent resources
    account_name: aiAccount.outputs.account_name
  }
}

var projectFullName = '${aiAccount.outputs.account_name}/${aiProject.outputs.projectName}'
// The Storage Blob Data Contributor role must be assigned before the caphost is created
module storageAccountRoleAssignment 'modules-standard/azure-storage-account-role-assignment.bicep' = {
  name: 'storage-${azureStorageName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(azureStorageSubscriptionId, azureStorageResourceGroupName)
  params: { 
    accountPrincipalId: aiAccount.outputs.accountPrincipalId
    azureStorageName: aiDependencies.outputs.azureStorageName
  }
  dependsOn: [
    aiProject
  ]
}

// The Comos DB Operator role must be assigned before the caphost is created
module cosmosAccountRoleAssignments 'modules-standard/cosmosdb-account-role-assignment.bicep' = {
  name: 'cosmos-account-role-assignments-${projectName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(cosmosDBSubscriptionId, cosmosDBResourceGroupName)
  params: {
    cosmosDBName: aiDependencies.outputs.cosmosDBName
    projectPrincipalId: aiProject.outputs.projectPrincipalId
  }
}

// This role can be assigned before or after the caphost is created
module aiSearchRoleAssignments 'modules-standard/ai-search-role-assignments.bicep' = {
  name: 'ai-search-role-assignments-${projectName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(aiSearchServiceSubscriptionId, aiSearchServiceResourceGroupName)
  params: {
    aiSearchName: aiDependencies.outputs.aiSearchName
    projectPrincipalId: aiProject.outputs.projectPrincipalId
  }
}

module addProjectCapabilityHost 'modules-standard/add-project-capability-host.bicep' = {
  name: 'capabilityHost-configuration-${projectName}-${uniqueSuffix}-deployment'
  params: {
    accountName: aiAccount.outputs.account_name
    projectFullName: projectFullName
    cosmosDBConnection: aiProject.outputs.cosmosDBConnection 
    azureStorageConnection: aiProject.outputs.azureStorageConnection
    aiSearchConnection: aiProject.outputs.aiSearchConnection

    projectCapHost: projectCapHost
    accountCapHost: accountCapHost
  }
  dependsOn: [
    aiSearchRoleAssignments, cosmosAccountRoleAssignments
  ]
}


module cosmosContainerRoleAssignments 'modules-standard/cosmos-container-role-assignments.bicep' = {
  name: 'cosmos-container-role-assignments-${projectName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(cosmosDBSubscriptionId, cosmosDBResourceGroupName)
  params: {
    cosmosAccountName: aiDependencies.outputs.cosmosDBName
    projectPrincipalId: aiProject.outputs.projectPrincipalId
    projectId: aiProject.outputs.projectId
}
dependsOn: [
  addProjectCapabilityHost
  ]
}

// The Storage Blob Data Contributor role must be assigned before the caphost is created
module storageContainersRoleAssignment 'modules-standard/blob-storage-container-role-assignments.bicep' = {
  name: 'storage-containers-role-assignment-${azureStorageName}-${uniqueSuffix}-deployment'
  scope: resourceGroup(azureStorageSubscriptionId, azureStorageResourceGroupName)
  params: { 
    projectPrincipalId: aiProject.outputs.projectPrincipalId
    azureStorageName: aiDependencies.outputs.azureStorageName
  }
  dependsOn: [
    addProjectCapabilityHost
  ]
}
