// Execute this main file to depoy Azure AI studio resources in the basic security configuraiton

// Parameters
@minLength(2)
@maxLength(12)
@description('Name for the AI resource and used to derive name of dependent resources.')
param aiHubName string = 'standard-hub'

@description('Friendly name for your Azure AI resource')
param aiHubFriendlyName string = 'Agents standard hub resource'

@description('Description of your Azure AI resource dispayed in AI studio')
param aiHubDescription string = 'A standard hub resource required for the agent setup.'
param aiProjectName string = 'standard-project'

@description('Friendly name for your Azure AI resource')
param aiProjectFriendlyName string = 'Agents standard project resource'

@description('Description of your Azure AI resource dispayed in AI studio')
param aiProjectDescription string = 'A standard project resource required for the agent setup.'


@description('Azure region used for the deployment of all resources.')
param location string = resourceGroup().location

@description('Set of tags to apply to all resources.')
param tags object = {}

// Variables
var name = toLower('${aiHubName}')
var projectName = toLower('${aiProjectName}')

@description('Name of the storage account')
param storageName string = 'agent-storage'

@description('Name of the Azure AI Services account')
param aiServicesName string = 'agent-ai-services'

// Create a short, unique suffix, that will be unique to each resource group
// var uniqueSuffix = substring(uniqueString(resourceGroup().id), 0, 4)
param deploymentTimestamp string = utcNow('yyyyMMddHHmmss')
var uniqueSuffix = substring(uniqueString('${resourceGroup().id}-${deploymentTimestamp}'), 0, 4)

// Dependent resources for the Azure Machine Learning workspace
module aiDependencies 'modules-standard/standard-dependent-resources.bicep' = {
  name: 'dependencies-${name}-${uniqueSuffix}-deployment'
  params: {
    aiServicesName: '${aiServicesName}${uniqueSuffix}'
    storageName: '${storageName}${uniqueSuffix}'
    location: location
    tags: tags
  }
}

module aiHub 'modules-standard/standard-ai-hub.bicep' = {
  name: '${name}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    aiHubName: 'ai-${name}-${uniqueSuffix}'
    aiHubFriendlyName: aiHubFriendlyName
    aiHubDescription: aiHubDescription
    location: location
    tags: tags

    // dependent resources
    storageAccountId: aiDependencies.outputs.storageId
    aiServicesId: aiDependencies.outputs.aiservicesID
    aiServicesTarget: aiDependencies.outputs.aiservicesTarget
  }
}

module aiProject 'modules-standard/standard-ai-project.bicep' = {
  name: 'ai-${projectName}-${uniqueSuffix}-deployment'
  params: {
    // workspace organization
    aiProjectName: 'ai-${projectName}-${uniqueSuffix}'
    aiProjectFriendlyName: aiProjectFriendlyName
    aiProjectDescription: aiProjectDescription
    location: location
    tags: tags

    // dependent resources
    aiHubId: aiHub.outputs.aiHubID
  }
}
