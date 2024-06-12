param name string
param properties object
param project_name string
param azure_openai_connection_name string

resource project 'Microsoft.MachineLearningServices/workspaces@2023-10-01' existing = {
  name: project_name
}

var defaults = {
  raiPolicyName: 'Microsoft.Default'
  versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  type: 'Azure.OpenAI'
  sku: {
    name: 'Standard'
    capacity: 20
  }
}

var properties_with_defaults = union(defaults, properties)

#disable-next-line BCP081
resource endpoint 'Microsoft.MachineLearningServices/workspaces/endpoints@2023-08-01-preview' existing = {
  parent: project
  name: azure_openai_connection_name

  #disable-next-line BCP081
  resource deployment 'deployments' = {
    name: name
    properties: {
      model: properties_with_defaults.model
      raiPolicyName: properties_with_defaults.raiPolicyName
      versionUpgradeOption: properties_with_defaults.versionUpgradeOption
      type: properties_with_defaults.type
      sku: properties_with_defaults.sku
    }
  }
}