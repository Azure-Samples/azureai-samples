// Creates an Azure AI resource with proxied endpoints for the Azure AI services provider

@description('Azure region of the deployment')
param location string

@description('Tags to add to the resources')
param tags object

@description('AI hub name')
param aiHubName string

@description('AI hub display name')
param aiHubFriendlyName string = aiHubName

@description('AI hub description')
param aiHubDescription string

@description('Resource ID of the storage account resource for storing experimentation outputs')
param storageAccountId string

@description('Resource ID of the AI Services resource')
param aiServicesId string

param aiServicesName string

@description('Resource ID of the AI Services endpoint')
param aiServicesTarget string

@description('Model/AI Resource deployment location')
param modelLocation string 

resource aiServices 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: aiServicesName
}

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-07-01-preview' = {
  name: aiHubName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    // organization
    friendlyName: aiHubFriendlyName
    description: aiHubDescription

    // dependent resources
    storageAccount: storageAccountId
  }
  kind: 'hub'

    resource aiServicesConnection 'connections@2024-07-01-preview' = {
    name: '${aiHubName}-connection-AIServices'
    properties: {
      category: 'AIServices'
      target: aiServicesTarget
      authType: 'AAD'
      isSharedToAll: true
      metadata: {
        ApiType: 'Azure'
        ResourceId: aiServicesId
        Location: modelLocation
      }
    }
  }

}

resource cognitiveServicesContributorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68'
  scope: resourceGroup()
}

resource cognitiveServicesContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01'= {
  scope: aiServices
  name: guid(aiServices.id, cognitiveServicesContributorRole.id, aiHub.id)
  properties: {  
    principalId: aiHub.identity.principalId
    roleDefinitionId: cognitiveServicesContributorRole.id
    principalType: 'ServicePrincipal'
  }
  }


resource cognitiveServicesOpenAIUserRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
  scope: resourceGroup()
}
resource cognitiveServicesOpenAIUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: aiServices
  name: guid(aiHub.id, cognitiveServicesOpenAIUserRole.id, aiServices.id)
  properties: {
    principalId: aiHub.identity.principalId
    roleDefinitionId: cognitiveServicesOpenAIUserRole.id
    principalType: 'ServicePrincipal'
  }
}

resource cognitiveServicesUserRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'a97b65f3-24c7-4388-baec-2e87135dc908'
  scope: resourceGroup()
}

resource cognitiveServicesUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: aiServices
  name: guid(aiHub.id, cognitiveServicesUserRole.id, aiServices.id)
  properties: {
    principalId: aiHub.identity.principalId
    roleDefinitionId: cognitiveServicesUserRole.id
    principalType: 'ServicePrincipal'
  }
}


output aiHubID string = aiHub.id
