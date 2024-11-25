@description('Specifies the name of the deployment.')
param name string

@description('Specifies the friendly name of the deployment.')
param nameFriendly string = name

@description('Specifies whether the workspace can be accessed by public networks or not.')
param publicNetworkAccess string = 'Enabled'

@description('Specifies the managedVnet IsolationMode')
@allowed([
  'Disabled'
  'AllowOnlyApprovedOutbound'
  'AllowInternetOutbound'
])
param isolationMode string = 'Disabled'

@description('AI services name')
param aiServicesName string = '${name}-aiservices'

@description('Determines whether or not a new container registry should be provisioned.')
@allowed([
  'new'
  'existing'
  'none'
])
param containerRegistryOption string = 'new'
param containerRegistryId string = 'null'
param defaultProjectResourceGroupId string = resourceGroup().id

@description('Specifies the location of the Azure Machine Learning workspace and dependent resources.')
param location string = resourceGroup().location

@description('Indicates whether or not the resourceId is OpenAI or AIServices.')
@allowed([
  'OpenAI'
  'AIServices'
])
param endpointKind string = 'AIServices'

@description('Determines whether or not an OpenAI endpoint should be provisioned.')
@allowed([
  'new'
  'none'
])
param endpointOption string = 'new'

@description('The name of the search service.')
param searchName string = ''

var uniqueSuffix = uniqueString(resourceGroup().id, name, nameFriendly)

module storageAccount 'storageAccount.bicep' = { name: 'storageAccount', params: { name: 'st${uniqueSuffix}', location: location } }
module keyVault 'keyvault.bicep' = { name: 'keyvault', params: { name: 'kv-${uniqueSuffix}', location: location } }
module containerRegistry 'container_registry.bicep' = if (containerRegistryOption == 'new') {
  name: 'containerRegistry', params: { name: 'cr${uniqueSuffix}', location: location }
}

@description('Either the user supplied ID, a new created one, or null')
var actualContainerRegistryId = (containerRegistryOption == 'new') ? containerRegistry.outputs.id : (containerRegistryOption == 'existing') ? containerRegistryId : null

resource workspace 'Microsoft.MachineLearningServices/workspaces@2023-02-01-preview' = {
  name: name
  location: location
  kind: 'Hub'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: nameFriendly
    storageAccount: storageAccount.outputs.id
    keyVault: keyVault.outputs.id
    containerRegistry: actualContainerRegistryId
    publicNetworkAccess: publicNetworkAccess
    #disable-next-line BCP037
    managedNetwork: {
      isolationMode: isolationMode
    }
    #disable-next-line BCP037
    workspaceHubConfig: {
      defaultWorkspaceResourceGroup: defaultProjectResourceGroupId
    }
  }
}

resource aiServices 'Microsoft.CognitiveServices/accounts@2021-10-01' = {
  name: aiServicesName
  location: location
  sku: {
    name: 'S0'
  }
  kind: endpointKind
  properties: {
    apiProperties: {
      statisticsEnabled: false
    }
  }
}

resource aiServicesConnection 'Microsoft.MachineLearningServices/workspaces/connections@2023-10-01' = {
  parent: workspace
  name: '${name}-connection-AzureOpenAI'
  properties: {
    category: 'AzureOpenAI'
    target: aiServices.properties.endpoint
    #disable-next-line BCP036
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: {
      key: aiServices.listKeys().key1
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: aiServices.id
    }
  }
}

resource workspaceName_Azure_Cognitive_Search 'Microsoft.MachineLearningServices/workspaces/connections@2023-10-01' = if (!empty(searchName)) {
  parent: workspace
  name: 'AzureAISearch'
  properties: {
    #disable-next-line BCP036
    authType: 'ApiKey'
    category: 'CognitiveSearch'
    credentials: {
      key: listAdminKeys(
        resourceId(subscription().subscriptionId, resourceGroup().name, 'Microsoft.Search/searchServices', searchName),
        '2020-08-01'
      ).primaryKey
    }
    metadata: { ApiType: 'Azure' }
    target: 'https://${searchName}.search.windows.net'
    value: '{"authType":"ApiKey","category":"AzureOpenAI","target":"https://${searchName}.search.windows.net"}'
  }
}

output id string = workspace.id
@description('The name of the workspace connection to the Search Service.')
output acs_connection_name string = (searchName != '') ? workspaceName_Azure_Cognitive_Search.name : ''
output azure_openai_endpoint string = aiServices.properties.endpoint
output azure_openai_connection_name string = (endpointOption == 'new') ? aiServicesConnection.name : ''