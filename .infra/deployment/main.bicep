targetScope = 'subscription'
param workspaceName string = 'azureai_samples_hub'
param projectName string = 'azureai_samples_proj'
param resourceGroupName string = 'rg-azureai-samples-validation-${utcNow('yyyyMM')}'

@description('The first day of the next month at deployment time in yyyy-MM-DD format.')
param __firstOfNextMonth string = '${dateTimeAdd('${utcNow('yyyy-MM')}-01 00:00:00Z', 'P31D', 'yyyy-MM')}-01'

param resourceGroupTags object = {
  SkipAutoDeleteTill: __firstOfNextMonth
}

param location string = 'eastus2'
@description('The ID of the principal (user, service principal, etc...) to create role assignments for.')
param principalId string = ''

@description('The Type of the principal (user, service principal, etc...) to create role assignments for.')
@allowed([ 'User', 'ServicePrincipal', '' ])
param principalType string = ''

var acsName = 'acs-samples-${uniqueString(rg.id, workspaceName, workspaceName)}'

resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  #disable-next-line use-stable-resource-identifiers
  name: resourceGroupName
  location: location
  tags: resourceGroupTags
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

var deployments = {
  gpt4: {
    name: 'gpt-4'
    properties: {
      model: {
        format: 'OpenAI'
        name: 'gpt-4'
        version: '1106-Preview'
      }
    }
  }

  text_embedding_ada_002: {
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
        capacity: 1
      }
    }
  }
}

var roleDefinitionIds = [
  'a001fd3d-188f-4b5d-821b-7da978bf7442' // Cognitive Services OpenAI Contributor
  'ba92f5b4-2d11-453d-a403-e96b0029c9fe' // Storage Blob Data Contributor
]

module role_assignments 'modules/role_assignment.bicep' = [for rd in roleDefinitionIds: if (!empty(principalId)) {
  name: 'role_assignment-${rd}'
  params: {
    principalId: principalId
    principalType: principalType
    roleDefinitionId: rd
  }
  scope: rg
}]

@batchSize(1)
module project_deployments 'modules/ai_project_deployment.bicep' = [for deployment in items(deployments): {
  name: 'project_deployment-${deployment.value.name}'
  params: {
    name: deployment.value.name
    properties: deployment.value.properties
    ai_services_name: workspace_hub.outputs.ai_services_name
  }
  scope: rg
}]

@description('The ID of the subscription deployed to.')
output subscription_id string = subscription().subscriptionId
@description('The name of the resource group deployed to.')
output resource_group_name string = rg.name
@description('The name of the Azure AI Project.')
output project_name string = project.outputs.name
output project_location string = project.outputs.location
output azure_openai_endpoint string = workspace_hub.outputs.azure_openai_endpoint
output azure_openai_gpt4_api_version string = '2024-08-01-preview'
output azure_openai_gpt4_deployment_name string = deployments.gpt4.name