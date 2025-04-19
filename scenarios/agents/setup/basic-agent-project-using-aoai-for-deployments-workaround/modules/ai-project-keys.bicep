
param account_name string
param location string
param project_name string
param projectDescription string  
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
    description: projectDescription
    displayName: display_name
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
// Azure AI Administrator Role -  Provides full access to manage AI resources and their settings
// Assign Project SMI - Azure AI Developer Role
// Most likely not permanent, but for now, this is the only way to assign the role to the project SMI
resource azureAIDeveloperRoleId 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '64702f94-c441-49e6-a78b-ef80e0188fee'  // Built-in role ID
  scope: resourceGroup()
}


resource projectSMIRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(azureAIDeveloperRoleId.id, account_name, account_name_resource.id, project_name)
  scope: account_name_project_name
  properties: {
    principalId: account_name_project_name.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: azureAIDeveloperRoleId.id
  }
}

output project_name string = account_name_project_name.name
output project_id string = account_name_project_name.id
output projectPrincipalId string = account_name_project_name.identity.principalId
