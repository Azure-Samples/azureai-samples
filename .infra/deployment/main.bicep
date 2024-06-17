targetScope = 'subscription'
param workspaceName string = 'azureai_samples_hub'
param projectName string = 'azureai_samples_proj'
param resourceGroupName string = 'azureai-samples-validation-${utcNow('yyyyMM')}'
param location string = 'westus'

var acsName = 'acs-samples-${uniqueString(rg.id, workspaceName, workspaceName)}'

resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  #disable-next-line use-stable-resource-identifiers
  name: resourceGroupName
  location: location
}

module acs 'modules/acs.bicep' = { name: 'acs', params: { name: acsName, location: location }, scope: rg }

module workspace_hub 'modules/workspace_hub.bicep' = {
  name: 'workspace-hub'
  params: {
    location: location
    name: workspaceName
    searchName: acs.outputs.name

  }
  scope: rg
}

module project 'modules/ai_project.bicep' = {
  name: 'project'
  params: {
    location: location
    workspaceHubID: workspace_hub.outputs.id
    name: projectName
  }
  scope: rg
}

var deployments = [
  {
    name: 'gpt-35-turbo'
    properties: {
      model: {
        format: 'OpenAI'
        name: 'gpt-35-turbo'
        version: '1106'
      }
    }
  }
  {
    name: 'text-embedding-ada-002'
    properties: {
      model: {
        format: 'OpenAI'
        name: 'text-embedding-ada-002'
        version: '2'
      }
      raiPolicyName: 'Microsoft.Default'
      versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
      type: 'Azure.OpenAI'
      sku: {
        name: 'Standard'
        capacity: 120
      }
    }
  }
]

module project_deployments 'modules/ai_project_deployment.bicep' = [for deployment in deployments: {
  name: 'project_deployment-${deployment.name}'
  params: {
    name: deployment.name
    properties: deployment.properties
    azure_openai_connection_name: workspace_hub.outputs.azure_openai_connection_name
    project_name: project.outputs.name
  }
  scope: rg
}]

@description('The ID of the subscription deployed to.')
output subscription_id string = subscription().subscriptionId
@description('The name of the resource group deployed to.')
output resource_group_name string = rg.name
@description('The name of the Azure AI Project.')
output project_name string = project.outputs.name
output acs_connection_name string = workspace_hub.outputs.acs_connection_name
