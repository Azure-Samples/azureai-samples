param account_name string
param location string
param project_name string
param projectDescription string  
param display_name string

param aiSearchName string
param aiSearchServiceResourceGroupName string
param aiSearchServiceSubscriptionId string

param cosmosDBName string
param cosmosDBSubscriptionId string
param cosmosDBResourceGroupName string

param azureStorageName string 
param azureStorageSubscriptionId string
param azureStorageResourceGroupName string

resource searchService 'Microsoft.Search/searchServices@2024-06-01-preview' existing = {
  name: aiSearchName
  scope: resourceGroup(aiSearchServiceSubscriptionId, aiSearchServiceResourceGroupName)
}
resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = {
  name: cosmosDBName
  scope: resourceGroup(cosmosDBSubscriptionId, cosmosDBResourceGroupName)
}
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' existing = {
  name: azureStorageName
  scope: resourceGroup(azureStorageSubscriptionId, azureStorageResourceGroupName)
}

var cosmosDBConnection = '${project_name}-cosmosconnection'
var azureStorageConnection = '${project_name}-storageconnection'
var aiSearchConnection = '${project_name}-searchconnection'

#disable-next-line BCP081
resource account_name_resource 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: account_name
  scope: resourceGroup()
}

#disable-next-line BCP081
resource account_name_project_name 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: account_name_resource
  name: project_name
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: projectDescription
    displayName: display_name
  }

  #disable-next-line BCP081
  resource project_connection_cosmosdb_account 'connections@2025-04-01-preview' = {
    name: cosmosDBConnection
    properties: {
      category: 'CosmosDB'
      target: 'https://${cosmosDBName}.documents.azure.com:443/'
      authType: 'AAD'
      metadata: {
        ApiType: 'Azure'
        ResourceId: cosmosDBAccount.id
        location: cosmosDBAccount.location
      }
    }
  }

  #disable-next-line BCP081
  resource project_connection_azure_storage 'connections@2025-04-01-preview' = {
    name: azureStorageConnection
    properties: {
      category: 'AzureStorageAccount'
      target: 'https://${azureStorageName}.blob.core.windows.net/'
      authType: 'AAD'
      isSharedToAll: true
      metadata: {
        ApiType: 'Azure'
        ResourceId: storageAccount.id
        location: storageAccount.location
      }
    }
  }

  #disable-next-line BCP081
  resource project_connection_azureai_search 'connections@2025-04-01-preview' = {
    name: aiSearchConnection
    properties: {
      category: 'CognitiveSearch'
      target: 'https://${aiSearchName}.search.windows.net'
      authType: 'AAD'
      metadata: {
        ApiType: 'Azure'
        ResourceId: searchService.id
        location: searchService.location
      }
    }
  }

  #disable-next-line BCP081
  resource project_connection_azure_openai 'connections@2025-04-01-preview' = {
    name: '${project_name}-accountconnection'
    properties: {
      authType: 'ApiKey'
      category: 'AzureOpenAI'
      target: account_name_resource.properties.endpoint
      credentials: {
        key: account_name_resource.listKeys('2025-04-01-preview').key1
      }
      isSharedToAll: true
      metadata: {
        ApiType: 'Azure'
        ResourceId: account_name_resource.id
        location: account_name_resource.location
      }
    }
  }
}

output projectName string = account_name_project_name.name
output projectId string = account_name_project_name.id
output projectPrincipalId string = account_name_project_name.identity.principalId

// return the BYO connection names
output cosmosDBConnection string = cosmosDBConnection
output azureStorageConnection string = azureStorageConnection
output aiSearchConnection string = aiSearchConnection
