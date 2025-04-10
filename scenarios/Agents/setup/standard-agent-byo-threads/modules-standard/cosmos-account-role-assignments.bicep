// Assigns the necessary roles to the AI project

@description('Name of the AI Search resource')
param cosmosDBName string

@description('Principal ID of the AI project')
param aiProjectPrincipalId string

param projectWorkspaceId string

#disable-next-line BCP081
resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2025-01-01-preview' existing = {
  name: cosmosDBName
  scope: resourceGroup()
}

resource cosmosDBOperatorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '230815da-be43-4aae-9cb4-875f7bd000aa'
  scope: resourceGroup()
}

resource cosmosDBOperatorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: cosmosDBAccount
  name: guid(projectWorkspaceId, cosmosDBOperatorRole.id, cosmosDBAccount.id)
  properties: {
    principalId: aiProjectPrincipalId
    roleDefinitionId: cosmosDBOperatorRole.id
    principalType: 'ServicePrincipal'
  }
}
