
param account_name string
param location string
param modelName string 
param modelFormat string 
param modelVersion string 
param modelSkuName string 
param modelCapacity int 



#disable-next-line BCP081
resource account_name_resource 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: account_name
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: account_name
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'

    // true is not supported today
    disableLocalAuth: false
  }
}

#disable-next-line BCP081
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview'=  {
  parent: account_name_resource
  name: modelName
  sku : {
    capacity: modelCapacity
    name: modelSkuName
  }
  properties: {
    model:{
      name: modelName
      format: modelFormat
      version: modelVersion
    }
  }
}

output account_name string = account_name_resource.name
output account_name_id string = account_name_resource.id
output aiServicesTarget string = account_name_resource.properties.endpoint
output accountPrincipalId string = account_name_resource.identity.principalId
