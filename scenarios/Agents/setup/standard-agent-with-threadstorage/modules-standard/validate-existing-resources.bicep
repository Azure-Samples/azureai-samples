@description('Resource ID of the AI Service Account. ')
param aiServiceAccountResourceId string

@description('Resource ID of the Azure AI Search Service.')
param aiSearchServiceResourceId string = ''

@description('Resource ID of the Azure Storage Account.')
param aiStorageAccountResourceId string = ''

@description('ResourceId of Cosmos DB Account')
param cosmosDBResourceId string = ''

var storagePassedIn = aiStorageAccountResourceId != ''
var aiServicesPassedIn = aiServiceAccountResourceId != ''
var searchPassedIn = aiSearchServiceResourceId != ''
var cosmosPassedIn = cosmosDBResourceId != ''


var aiServiceParts = split(aiServiceAccountResourceId, '/')
var aiServiceAccountSubscriptionId = aiServicesPassedIn ? aiServiceParts[2] : subscription().subscriptionId
var aiServiceAccountResourceGroupName = aiServicesPassedIn ? aiServiceParts[4] : resourceGroup().name

var acsParts = split(aiSearchServiceResourceId, '/')
var aiSearchServiceSubscriptionId = searchPassedIn ? acsParts[2] : subscription().subscriptionId
var aiSearchServiceResourceGroupName = searchPassedIn ? acsParts[4] : resourceGroup().name

var cosmosParts = split(cosmosDBResourceId, '/')
var cosmosDBSubscriptionId = cosmosPassedIn ? cosmosParts[2] : subscription().subscriptionId
var cosmosDBResourceGroupName = cosmosPassedIn ? cosmosParts[4] : resourceGroup().name

var storageParts = split(aiStorageAccountResourceId, '/')
var azureStorageSubscriptionId = storagePassedIn ? storageParts[2] : subscription().subscriptionId
var azureStorageResourceGroupName = storagePassedIn ? storageParts[4] : resourceGroup().name

resource aiServiceAccount 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' existing = if (aiServicesPassedIn) {
  name: last(split(aiServiceAccountResourceId, '/'))
  scope: resourceGroup(aiServiceAccountSubscriptionId, aiServiceAccountResourceGroupName)
}

// Validate Azure AI Search
resource azureAISearch 'Microsoft.Search/searchServices@2024-06-01-preview' existing = if (searchPassedIn) {
  name: last(split(aiSearchServiceResourceId, '/'))
  scope: resourceGroup(aiSearchServiceSubscriptionId, aiSearchServiceResourceGroupName)
}


// Validate Cosmos DB Account
resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = if (cosmosPassedIn) {
  name: last(split(cosmosDBResourceId, '/'))
  scope: resourceGroup(cosmosDBSubscriptionId,cosmosDBResourceGroupName)
}

// Validate Storage Account
resource azureStorageAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = if (storagePassedIn) {
  name: storageParts[8]
  scope: resourceGroup(azureStorageSubscriptionId,azureStorageResourceGroupName)
}

output aiServiceExists bool = aiServicesPassedIn && (aiServiceAccount.name == aiServiceParts[8])
output aiSearchExists bool = searchPassedIn && (azureAISearch.name == acsParts[8])
output cosmosDBExists bool = cosmosPassedIn && (cosmosDBAccount.name == cosmosParts[8])
output aiStorageExists bool = storagePassedIn && (azureStorageAccount.name == storageParts[8])

output aiSearchServiceSubscriptionId string = aiSearchServiceSubscriptionId
output aiSearchServiceResourceGroupName string = aiSearchServiceResourceGroupName

output cosmosDBSubscriptionId string = cosmosDBSubscriptionId
output cosmosDBResourceGroupName string = cosmosDBResourceGroupName

output aiServiceAccountSubscriptionId string = aiServiceAccountSubscriptionId
output aiServiceAccountResourceGroupName string = aiServiceAccountResourceGroupName

output azureStorageSubscriptionId string = azureStorageSubscriptionId
output azureStorageResourceGroupName string = azureStorageResourceGroupName
