// Creates an Azure AI resource with proxied endpoints for the Azure AI services provider

@description('Azure region of the deployment')
param location string

@description('Tags to add to the resources')
param tags object

@description('AI Project name')
param aiProjectName string

@description('AI Project display name')
param aiProjectFriendlyName string = aiProjectName

@description('AI Project description')
param aiProjectDescription string

@description('Resource ID of the AI Hub resource')
param aiHubId string

@description('The name of the CosmosDB account')
param cosmosDBName string

@description('Subscription ID of the Cosmos DB resource')
param cosmosDBSubscriptionId string

@description('Resource Group name of the Cosmos DB resource')
param cosmosDBResourceGroupName string

//for constructing endpoint
var subscriptionId = subscription().subscriptionId
var resourceGroupName = resourceGroup().name

var projectConnectionString = '${location}.api.azureml.ms;${subscriptionId};${resourceGroupName};${aiProjectName}'

var cosmosConnectionName = '${aiProjectName}-connection-CosmosDBAccount'

resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = {
  name: cosmosDBName
  scope: resourceGroup(cosmosDBSubscriptionId,cosmosDBResourceGroupName)
}

#disable-next-line BCP081
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-10-01-preview' = {
  name: aiProjectName
  location: 'eastus2euap'
  tags: union(tags, {
    ProjectConnectionString: projectConnectionString
  })
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    // organization
    friendlyName: aiProjectFriendlyName
    description: aiProjectDescription

    // dependent resources
    hubResourceId: aiHubId

  }
  kind: 'project'
}

#disable-next-line BCP081
resource project_connection_cosmosdb 'Microsoft.MachineLearningServices/workspaces/connections@2025-01-01-preview' = {
  name: cosmosConnectionName
  parent: aiProject
  properties: {
    category: 'CosmosDB'
    target: 'https://${cosmosDBName}documents.azure.com:443/'
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: cosmosDBAccount.id
      location: cosmosDBAccount.location
    }
  }
}

output cosmosConnectionName string = project_connection_cosmosdb.name
output aiProjectName string = aiProject.name
output aiProjectResourceId string = aiProject.id
output aiProjectPrincipalId string = aiProject.identity.principalId
output aiProjectWorkspaceId string = aiProject.properties.workspaceId
output projectConnectionString string = aiProject.tags.ProjectConnectionString
