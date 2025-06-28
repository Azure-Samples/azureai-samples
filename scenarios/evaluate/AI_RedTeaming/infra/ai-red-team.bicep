@description('Azure region of the deployment')
param location string

@description('Tags to add to the resources')
param tags object

@description('Resource token to use for unique resource names')
param resourceToken string

@description('Id of the user or app to assign application roles')
param principalId string

@description('Whether to create role assignments for the principal')
param createRoleAssignments bool = false

// Variables for naming
var aiFoundryName = 'aifoundry-${resourceToken}'
var aiProjectName = 'aiproject-${resourceToken}'
var keyVaultName = 'kv-${resourceToken}'
var storageAccountName = 'stor${resourceToken}'
var searchServiceName = 'search-${resourceToken}'
var logAnalyticsName = 'log-${resourceToken}'
var appInsightsName = 'appi-${resourceToken}'

// Create Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enablePurgeProtection: true  // Changed from false to true - required by Azure policy
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Create Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    defaultToOAuthAuthentication: false
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      defaultAction: 'Allow'
    }
    publicNetworkAccess: 'Enabled'
    supportsHttpsTrafficOnly: true
  }
}

// Create Log Analytics workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      searchVersion: 1
      legacy: 0
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Create Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Remove the separate OpenAI account since models are deployed directly on AI Foundry
// The OpenAI functionality is now provided through the AI Foundry account

// Deploy OpenAI models
// Note: Models are now deployed as part of the AI Foundry account resource above

// Create Azure AI Search service
resource searchService 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: searchServiceName
  location: location
  tags: tags
  sku: {
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    networkRuleSet: {
      ipRules: []
    }
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    disableLocalAuth: false
    authOptions: {
      apiKeyOnly: {}
    }
  }
}

/*
  An AI Foundry resources is a variant of a CognitiveServices/account resource type
*/ 
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiFoundryName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'  }
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
    // required to work in AI Foundry
    allowProjectManagement: true 

    // Defines developer API endpoint subdomain
    customSubDomainName: aiFoundryName

    // Enable local auth to allow key listing for outputs
    disableLocalAuth: false
    
    // Add required publicNetworkAccess property
    publicNetworkAccess: 'Enabled'
    
    // Add required networkAcls configuration
    networkAcls: {
      defaultAction: 'Allow'
      ipRules: []
      virtualNetworkRules: []
    }
  }
}

/*
  Developer APIs are exposed via a project, which groups in- and outputs that relate to one use case, including files.
  Its advisable to create one project right away, so development teams can directly get started.
  Projects may be granted individual RBAC permissions and identities on top of what account provides.
*/ 
resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: aiProjectName
  parent: aiFoundry
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

/*
  Optionally deploy a model to use in playground, agents and other tools.
*/
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
  parent: aiFoundry
  name: 'gpt-4o'
  sku : {
    capacity: 1
    name: 'GlobalStandard'
  }
  properties: {
    model:{
      name: 'gpt-4o'
      format: 'OpenAI'
    }
  }
}

// RBAC Role Definitions
var roleDefinitionIds = {
  Owner: '8e3af657-a8ff-443c-a75c-2fe8c4bcb635'
  Contributor: 'b24988ac-6180-42a0-ab88-20f7382dd24c'
  Reader: 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
  'Storage Blob Data Contributor': 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  'Storage Blob Data Reader': '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
  'Cognitive Services OpenAI User': '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
  'Cognitive Services User': 'a97b65f3-24c7-4388-baec-2e87135dc908'
  'Cognitive Services Contributor': '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68'
  'Search Index Data Contributor': '8ebe5a00-799e-43f5-93ac-243d3dce84a7'
  'Search Service Contributor': '7ca78c08-252a-4471-8644-bb5ff32d4ba0'
  'Key Vault Secrets User': '4633458b-17de-408a-b874-0445c86b69e6'
  'AzureML Data Scientist': 'f6c7c914-8db3-469d-8ca1-694a8f32e121'
}

// Assign roles to the user/service principal if provided
resource storageRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments && !empty(principalId)) {
  scope: storageAccount
  name: guid(storageAccount.id, principalId, roleDefinitionIds['Storage Blob Data Contributor'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Storage Blob Data Contributor'])
    principalId: principalId
    principalType: 'User'
  }
}

resource aiFoundryRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments && !empty(principalId)) {
  scope: aiFoundry
  name: guid(aiFoundry.id, principalId, roleDefinitionIds['Cognitive Services OpenAI User'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Cognitive Services OpenAI User'])
    principalId: principalId
    principalType: 'User'
  }
}

resource searchRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments && !empty(principalId)) {
  scope: searchService
  name: guid(searchService.id, principalId, roleDefinitionIds['Search Index Data Contributor'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Search Index Data Contributor'])
    principalId: principalId
    principalType: 'User'
  }
}

resource keyVaultRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments && !empty(principalId)) {
  scope: keyVault
  name: guid(keyVault.id, principalId, roleDefinitionIds['Key Vault Secrets User'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Key Vault Secrets User'])
    principalId: principalId
    principalType: 'User'
  }
}

resource aiProjectRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments && !empty(principalId)) {
  scope: aiFoundry  // Assign role to AI Foundry account instead of project
  name: guid(aiFoundry.id, principalId, roleDefinitionIds['Cognitive Services User'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Cognitive Services User'])
    principalId: principalId
    principalType: 'User'
  }
}

// Add Cognitive Services Contributor role for red team operations
resource aiFoundryContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments && !empty(principalId)) {
  scope: aiFoundry
  name: guid(aiFoundry.id, principalId, roleDefinitionIds['Cognitive Services Contributor'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Cognitive Services Contributor'])
    principalId: principalId
    principalType: 'User'
  }
}

// Assign AI Foundry managed identity permissions (conditional)
resource aiFoundryStorageRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments) {
  scope: storageAccount
  name: guid(storageAccount.id, aiFoundry.id, roleDefinitionIds['Storage Blob Data Contributor'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Storage Blob Data Contributor'])
    principalId: aiFoundry.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource aiFoundryKeyVaultRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments) {
  scope: keyVault
  name: guid(keyVault.id, aiFoundry.id, roleDefinitionIds['Key Vault Secrets User'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Key Vault Secrets User'])
    principalId: aiFoundry.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Assign AI Project managed identity permissions (conditional)
resource aiProjectStorageRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments) {
  scope: storageAccount
  name: guid(storageAccount.id, aiProject.id, roleDefinitionIds['Storage Blob Data Contributor'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Storage Blob Data Contributor'])
    principalId: aiProject.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource aiProjectFoundryRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (createRoleAssignments) {
  scope: aiFoundry
  name: guid(aiFoundry.id, aiProject.id, roleDefinitionIds['Cognitive Services OpenAI User'])
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionIds['Cognitive Services OpenAI User'])
    principalId: aiProject.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Outputs
output aiFoundryName string = aiFoundry.name
output aiProjectName string = aiProject.name
output aiProjectEndpoint string = 'https://${aiFoundry.name}.services.ai.azure.com/api/projects/${aiProject.name}'
output aiFoundryEndpoint string = 'https://${aiFoundry.name}.services.ai.azure.com'
output openAiEndpoint string = aiFoundry.properties.endpoint
output openAiApiKey string = aiFoundry.listKeys().key1
output storageAccountName string = storageAccount.name
output storageConnectionString string = 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=${environment().suffixes.storage}'
output keyVaultName string = keyVault.name
output searchServiceName string = searchService.name
output searchServiceEndpoint string = 'https://${searchService.name}.search.windows.net/'
output searchServiceApiKey string = searchService.listAdminKeys().primaryKey