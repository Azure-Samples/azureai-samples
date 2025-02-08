param name string
param nameFriendly string = name
param workspaceHubID string
param location string = resourceGroup().location

resource project 'Microsoft.MachineLearningServices/workspaces@2023-10-01' = {
  name: name
  #disable-next-line BCP187
  kind: 'Project'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: nameFriendly
    #disable-next-line BCP037
    hubResourceId: workspaceHubID
  }
}

output name string = project.name
output location string = project.location