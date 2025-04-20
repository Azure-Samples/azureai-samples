param account_name string = 'aiServices${substring(uniqueString(utcNow()), 0,4)}'
param project_name string = 'project'
param projectDescription string = 'some description'
param projectDisplayName string = 'project_display_name'
param location string = 'westus2'

param modelName string = 'gpt-4o'
param modelFormat string = 'OpenAI'
param modelVersion string = '2024-11-20'
param modelSkuName string = 'GlobalStandard'
param modelCapacity int = 30

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
    disableLocalAuth: false
  }
}

/*
  Step 2: Deploy gpt-4o model
  
  - Agents will use the build-in model deployments
*/ 

#disable-next-line BCP081
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
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

/*
  Step 3: Create a Cognitive Services Project
    
*/
#disable-next-line BCP081
resource account_name_project_name 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: account_name_resource
  name: '${project_name}'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: projectDescription
    displayName: projectDisplayName
  }
}

output ENDPOINT string = account_name_resource.properties.endpoint
output project_name string = account_name_project_name.name
output account_name string = account_name_resource.name
