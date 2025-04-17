@description('AI hub name')
param aiHubName string

@description('AI project name')
param aiProjectName string

@description('Name for ACS connection.')
param acsConnectionName string

@description('Name for ACS connection.')
param aoaiConnectionName string

@description('Name for capabilityHost.')
param capabilityHostName string 

@description('Name for CosmosDB connection.')
param cosmosConnectionName string

var storageConnections = ['${aiProjectName}/workspaceblobstore']
var aiSearchConnection = ['${acsConnectionName}']
var aiServiceConnections = ['${aoaiConnectionName}']
var cosmosDBConnections = ['${cosmosConnectionName}']

#disable-next-line BCP081
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-10-01-preview' existing = {
  name: aiHubName
}

#disable-next-line BCP081
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-10-01-preview' existing = {
  name: aiProjectName
}

#disable-next-line BCP081
resource hubCapabilityHost 'Microsoft.MachineLearningServices/workspaces/capabilityHosts@2025-01-01-preview' = {
  name: '${aiHubName}-${capabilityHostName}'
  parent: aiHub
  properties: {
     capabilityHostKind: 'Agents'
  }
}

#disable-next-line BCP081
resource projectCapabilityHost 'Microsoft.MachineLearningServices/workspaces/capabilityHosts@2025-01-01-preview' = {
  name: '${aiProjectName}-${capabilityHostName}'
  parent: aiProject
  properties: {
    capabilityHostKind: 'Agents'
    aiServicesConnections: aiServiceConnections
    vectorStoreConnections: aiSearchConnection
    storageConnections: storageConnections
    threadStorageConnections: cosmosDBConnections
  }
  dependsOn: [
    hubCapabilityHost
  ]
}
