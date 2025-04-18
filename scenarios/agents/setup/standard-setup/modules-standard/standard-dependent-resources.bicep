// Creates Azure dependent resources for Azure AI Agent Service standard agent setup

@description('Azure region of the deployment')
param location string

// @description('The name of the Key Vault')
// param keyvaultName string

@description('The name of the AI Search resource')
param aiSearchName string

@description('Name of the storage account')
param azureStorageName string

@description('Name of the new Cosmos DB account')
param cosmosDBName string

@description('The AI Search Service full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param aiSearchResourceId string

@description('The AI Storage Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param azureStorageAccountResourceId string

@description('The Cosmos DB Account full ARM Resource ID. This is an optional field, and if not provided, the resource will be created.')
param cosmosDBResourceId string

// param aiServiceExists bool
param aiSearchExists bool
param azureStorageExists bool
param cosmosDBExists bool


var cosmosParts = split(cosmosDBResourceId, '/')

resource existingCosmosDB 'Microsoft.DocumentDB/databaseAccounts@2024-11-15' existing = if (cosmosDBExists) {
  name: cosmosParts[8]
  scope: resourceGroup(cosmosParts[2], cosmosParts[4])
}

var canaryRegions = ['eastus2euap', 'centraluseuap']
var cosmosDbRegion = contains(canaryRegions, location) ? 'westus' : location
resource cosmosDB 'Microsoft.DocumentDB/databaseAccounts@2024-11-15' = if(!cosmosDBExists) {
  name: cosmosDBName
  location: cosmosDbRegion
  kind: 'GlobalDocumentDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    disableLocalAuth: true
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    enableFreeTier: false
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    databaseAccountOfferType: 'Standard'
  }
}


// resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
//   name: keyvaultName
//   location: location
//   tags: tags
//   properties: {
//     createMode: 'default'
//     enabledForDeployment: false
//     enabledForDiskEncryption: false
//     enabledForTemplateDeployment: false
//     enableSoftDelete: true
//     enableRbacAuthorization: true
//     enablePurgeProtection: true
//     networkAcls: {
//       bypass: 'AzureServices'
//       defaultAction: 'Deny'
//     }
//     sku: {
//       family: 'A'
//       name: 'standard'
//     }
//     softDeleteRetentionInDays: 7
//     tenantId: subscription().tenantId
//   }
// }


// var aiServiceParts = split(aiServiceAccountResourceId, '/')

// resource existingAIServiceAccount 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = if (aiServiceExists) {
//   name: aiServiceParts[8]
//   scope: resourceGroup(aiServiceParts[2], aiServiceParts[4])
// }

// resource aiServices 'Microsoft.CognitiveServices/accounts@2024-10-01' = if(!aiServiceExists) {
//   name: aiServicesName
//   location: modelLocation
//   sku: {
//     name: 'S0'
//   }
//   kind: 'AIServices' // or 'OpenAI'
//   identity: {
//     type: 'SystemAssigned'
//   }
//   properties: {
//     customSubDomainName: toLower('${(aiServicesName)}')
//     apiProperties: {
//       statisticsEnabled: false
//     }
//     publicNetworkAccess: 'Enabled'
//   }
// }
// resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= if(!aiServiceExists){
//   parent: aiServices
//   name: modelName
//   sku : {
//     capacity: modelCapacity
//     name: modelSkuName
//   }
//   properties: {
//     model:{
//       name: modelName
//       format: modelFormat
//       version: modelVersion
//     }
//   }
// }

var acsParts = split(aiSearchResourceId, '/')

resource existingSearchService 'Microsoft.Search/searchServices@2024-06-01-preview' existing = if (aiSearchExists) {
  name: acsParts[8]
  scope: resourceGroup(acsParts[2], acsParts[4])
}
resource aiSearch 'Microsoft.Search/searchServices@2024-06-01-preview' = if(!aiSearchExists) {
  name: aiSearchName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    disableLocalAuth: false
    authOptions: { aadOrApiKey: { aadAuthFailureMode: 'http401WithBearerChallenge'}}
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    hostingMode: 'default'
    partitionCount: 1
    publicNetworkAccess: 'enabled'
    replicaCount: 1
    semanticSearch: 'disabled'
  }
  sku: {
    name: 'standard'
  }
}

var azureStorageParts = split(azureStorageAccountResourceId, '/')

resource existingAzureStorageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' existing = if (azureStorageExists) {
  name: azureStorageParts[8]
  scope: resourceGroup(azureStorageParts[2], azureStorageParts[4])
}

// Some regions doesn't support Standard Zone-Redundant storage, need to use Geo-redundant storage
param noZRSRegions array = ['southindia', 'westus']
param sku object = contains(noZRSRegions, location) ? { name: 'Standard_GRS' } : { name: 'Standard_ZRS' }

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = if(!azureStorageExists) {
  name: azureStorageName
  location: location
  kind: 'StorageV2'
  sku: sku
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
      virtualNetworkRules: []
    }
    allowSharedKeyAccess: false
  }
}

// output aiServicesName string =  aiServiceExists ? existingAIServiceAccount.name : aiServicesName
// output aiservicesID string = aiServiceExists ? existingAIServiceAccount.id : aiServices.id
// output aiservicesTarget string = aiServiceExists ? existingAIServiceAccount.properties.endpoint : aiServices.properties.endpoint
// output aiServiceAccountResourceGroupName string = aiServiceExists ? aiServiceParts[4] : resourceGroup().name
// output aiServiceAccountSubscriptionId string = aiServiceExists ? aiServiceParts[2] : subscription().subscriptionId

output aiSearchName string = aiSearchExists ? existingSearchService.name : aiSearch.name
output aiSearchID string = aiSearchExists ? existingSearchService.id : aiSearch.id
output aiSearchServiceResourceGroupName string = aiSearchExists ? acsParts[4] : resourceGroup().name
output aiSearchServiceSubscriptionId string = aiSearchExists ? acsParts[2] : subscription().subscriptionId

output azureStorageName string = azureStorageExists ? existingAzureStorageAccount.name :  storage.name
output azureStorageId string =  azureStorageExists ? existingAzureStorageAccount.id :  storage.id
output azureStorageResourceGroupName string = azureStorageExists ? azureStorageParts[4] : resourceGroup().name
output azureStorageSubscriptionId string = azureStorageExists ? azureStorageParts[2] : subscription().subscriptionId

output cosmosDBName string = cosmosDBExists ? existingCosmosDB.name : cosmosDB.name
output cosmosDBId string = cosmosDBExists ? existingCosmosDB.id : cosmosDB.id
output cosmosDBResourceGroupName string = cosmosDBExists ? cosmosParts[4] : resourceGroup().name
output cosmosDBSubscriptionId string = cosmosDBExists ? cosmosParts[2] : subscription().subscriptionId

// output keyvaultId string = keyVault.id
