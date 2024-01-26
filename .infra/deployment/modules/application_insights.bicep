param name string
param logWorkspaceName string
param location string = resourceGroup().location

var actualLocation = (((location == 'westcentralus') || (location == 'eastus2euap') || (location == 'centraluseuap')) ? 'southcentralus' : location)

resource appInsightsLogWorkspace 'Microsoft.OperationalInsights/workspaces@2020-08-01' = {
  name: name
  location: actualLocation
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: logWorkspaceName
  location: actualLocation
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: appInsightsLogWorkspace.id
  }
}

output id string = applicationInsights.id