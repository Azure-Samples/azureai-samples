param cosmosDBConnection string 
param azureStorageConnection string 
param aiSearchConnection string
param project_name string
param account_name string
param projectCapHost string
param accountCapHost string

var threadConnections = ['${cosmosDBConnection}']
var storageConnections = ['${azureStorageConnection}']
var vectorStoreConnections = ['${aiSearchConnection}']

#disable-next-line BCP081
resource account_name_resource 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: account_name
  scope: resourceGroup()
}

#disable-next-line BCP081
resource account_name_capHost_resource 'Microsoft.CognitiveServices/accounts/capabilityHosts@2025-04-01-preview' = {
  name: accountCapHost
  parent: account_name_resource
  properties: {
    capabilityHostKind: 'Agents'
   
  }
}

resource account_name_project_name 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  name: project_name
  scope: resourceGroup()
}

#disable-next-line BCP081
resource account_name_project_name_capHost 'Microsoft.CognitiveServices/accounts/projects/capabilityHosts@2025-04-01-preview' = {
  name: projectCapHost
  parent: account_name_project_name
  properties: {
    capabilityHostKind: 'Agents'
    vectorStoreConnections: vectorStoreConnections
    storageConnections: storageConnections
    threadStorageConnections: threadConnections
  }
}
