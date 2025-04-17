
param account_name string
param location string
param project_name string
param description string  
param display_name string

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
    description: description
    displayName: display_name
  }
}

output project_name string = account_name_project_name.name
output project_id string = account_name_project_name.id
output projectPrincipalId string = account_name_project_name.identity.principalId
