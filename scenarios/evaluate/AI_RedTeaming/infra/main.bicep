targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string = ''

// Tags that should be applied to all resources.
var tags = {
  'azd-env-name': environmentName
  'ai-toolkit': 'red-teaming'
}

// Generate a unique token to be used in naming resources.
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

// Name of the resource group for the AI Red Teaming resources
var resourceGroupName = 'rg-${environmentName}-${resourceToken}'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module aiRedTeam 'ai-red-team.bicep' = {
  name: 'ai-red-team'
  scope: rg
  params: {
    location: location
    tags: tags
    resourceToken: resourceToken
    principalId: principalId
    createRoleAssignments: false
  }
}

// Outputs - Standard Azure environment variables
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_SUBSCRIPTION_ID string = subscription().subscriptionId
output AZURE_RESOURCE_GROUP string = rg.name

// Primary outputs for .env file generation
output AZURE_AI_PROJECT string = aiRedTeam.outputs.aiProjectEndpoint
output AZURE_OPENAI_CONFIG string = '{"endpoint": "${aiRedTeam.outputs.openAiEndpoint}", "api_key": "${aiRedTeam.outputs.openAiApiKey}", "deployment": "gpt-4o", "api_version": "2024-10-21"}'
output AZURE_STORAGE_ACCOUNT string = aiRedTeam.outputs.storageAccountName

// Additional resource outputs for debugging and advanced use cases
output AI_FOUNDRY_NAME string = aiRedTeam.outputs.aiFoundryName
output AI_PROJECT_NAME string = aiRedTeam.outputs.aiProjectName
output AI_FOUNDRY_ENDPOINT string = aiRedTeam.outputs.aiFoundryEndpoint
output AZURE_OPENAI_ENDPOINT string = aiRedTeam.outputs.openAiEndpoint
output AZURE_OPENAI_API_KEY string = aiRedTeam.outputs.openAiApiKey
output AZURE_STORAGE_ACCOUNT_NAME string = aiRedTeam.outputs.storageAccountName
output AZURE_STORAGE_CONNECTION_STRING string = aiRedTeam.outputs.storageConnectionString
output SEARCH_SERVICE_NAME string = aiRedTeam.outputs.searchServiceName
output SEARCH_SERVICE_ENDPOINT string = aiRedTeam.outputs.searchServiceEndpoint
output SEARCH_SERVICE_API_KEY string = aiRedTeam.outputs.searchServiceApiKey
output KEY_VAULT_NAME string = aiRedTeam.outputs.keyVaultName
