param projectPrincipalId string
param azureStorageName string

@description('Role Definition ID for Storage Blob Data Owner')
var storageBlobDataOwnerRoleId = 'b7e6dc6d-f1e8-4753-8033-0f276bb0955b'

@description('Name of the container to assign the role')
var agentContainerName = '${projectPrincipalId}-azureml-agent'

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' existing = {
  name: azureStorageName
  scope: resourceGroup()
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2022-05-01' existing = {
  name: agentContainerName
  scope: resourceGroup()
}

resource storageBlobDataOwnerAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: blobContainer
  name: guid(blobContainer.id, storageBlobDataOwnerRoleId, projectPrincipalId, storageAccount.id)
  properties: {
    principalId: projectPrincipalId
    roleDefinitionId: storageBlobDataOwnerRoleId
    principalType: 'ServicePrincipal'
  }
}

