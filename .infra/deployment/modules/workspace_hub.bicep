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

@description('Determines whether or not new ApplicationInsights should be provisioned.')
@allowed([
  'new'
  'existing'
  'none'
])
param applicationInsightsOption string = 'new'
param applicationInsightId string = 'null'

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
module applicationInsights 'application_insights.bicep' = if (applicationInsightsOption == 'new') {
  name: 'applicationInsights', params: { name: 'appi-${uniqueSuffix}', logWorkspaceName: 'apws-${uniqueSuffix}', location: location }
}

@description('Either the user supplied ID, a new created one, or null')
var actualContainerRegistryId = (containerRegistryOption == 'new') ? containerRegistry.outputs.id : (containerRegistryOption == 'existing') ? containerRegistryId : null

@description('Either the user supplied ID, a new created one, or null')
var actualApplicationInsightsId = (applicationInsightsOption == 'new') ? applicationInsights.outputs.id : (applicationInsightsOption == 'existing') ? applicationInsightId : null

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
    applicationInsights: actualApplicationInsightsId
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

#disable-next-line BCP081
resource workspaceName_Azure_OpenAI 'Microsoft.MachineLearningServices/workspaces/endpoints@2023-08-01-preview' = if (endpointOption == 'new') {
  parent: workspace
  name: 'Azure.OpenAI'
  properties: {
    name: 'Azure.OpenAI'
    endpointType: 'Azure.OpenAI'
    associatedResourceId: null
  }
}

#disable-next-line BCP081
resource workspaceName_Azure_ContentSafety 'Microsoft.MachineLearningServices/workspaces/endpoints@2023-08-01-preview' = if ((endpointKind == 'AIServices') && (endpointOption == 'new')) {
  parent: workspace
  name: 'Azure.ContentSafety'
  properties: {
    name: 'Azure.ContentSafety'
    endpointType: 'Azure.ContentSafety'
    associatedResourceId: null
  }
}

#disable-next-line BCP081
resource workspaceName_Azure_Speech 'Microsoft.MachineLearningServices/workspaces/endpoints@2023-08-01-preview' = if ((endpointKind == 'AIServices') && (endpointOption == 'new')) {
  parent: workspace
  name: 'Azure.Speech'
  properties: {
    name: 'Azure.Speech'
    endpointType: 'Azure.Speech'
    associatedResourceId: null
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
output azure_openai_endpoint string = workspaceName_Azure_OpenAI.properties.endpointUri
output openai_endpoint_name string = (endpointOption == 'new') ? workspaceName_Azure_OpenAI.name : ''