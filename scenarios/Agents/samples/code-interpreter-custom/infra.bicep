@description('Suffix for resource names to ensure uniqueness')
@minLength(3)
param suffix string = uniqueString(resourceGroup().id)

@description('Container Apps environment name')
@minLength(3)
param environmentName string = 'aca-env-${suffix}'

@description('Session pool name')
@minLength(3)
param sessionPoolName string = 'sp-${suffix}'

@description('The amount of CPU to provide to each container instance, in vCPU counts')
@minValue(1)
@maxValue(16)
param cpu int = 1

@description('The amount of RAM to provide to each container instance, in GiB')
@minValue(1)
@maxValue(16)
param memory int = 2

@description('Location of all ACA resources.')
@allowed([
  'eastus'
  'swedencentral'
  'northeurope'
])
param location string = 'swedencentral'

@description('Use managed identity for deployment script principal')
param useManagedIdentity bool = true

@description('An image that implements the code interpreter HTTP API')
param image string = 'mcr.microsoft.com/k8se/services/codeinterpreter:0.9.18-python3.12'

@description('Model deployment name')
param modelDeploymentName string = 'my-gpt-4o-mini'

@description('Model to deploy')
param modelName string = 'gpt-4o-mini'

resource environment 'Microsoft.App/managedEnvironments@2025-10-02-preview' = {
  name: environmentName
  location: location
  properties: {
    workloadProfiles: [
      {
        name: 'Consumption'
        workloadProfileType: 'Consumption'
      }
    ]
  }
}

resource sessionPool 'Microsoft.App/sessionPools@2025-10-02-preview' = {
  name: sessionPoolName
  location: location
  properties: {
    environmentId: environment.id
    poolManagementType: 'Dynamic'
    containerType: 'CustomContainer'
    scaleConfiguration: {
      maxConcurrentSessions: 10
      readySessionInstances: 5
    }
    dynamicPoolConfiguration: {
      lifecycleConfiguration: {
        cooldownPeriodInSeconds: 600
        lifecycleType: 'Timed'
      }
    }
    customContainerTemplate: {
      containers: [
        {
          name: 'jupyterpython'
          image: image
          env: [
            {
              name: 'SYS_RUNTIME_SANDBOX'
              value: 'AzureContainerApps-DynamicSessions'
            }
            {
              name: 'AZURE_CODE_EXEC_ENV'
              value: 'AzureContainerApps-DynamicSessions-Py3.12'
            }
            {
              name: 'AZURECONTAINERAPPS_SESSIONS_SANDBOX_VERSION'
              value: '7758'
            }
            {
              name: 'JUPYTER_TOKEN'
              value: 'AzureContainerApps-DynamicSessions'
            }
          ]
          resources: {
            cpu: cpu
            memory: '${memory}Gi'
          }
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/health'
                port: 6000
              }
              failureThreshold: 4
            }
            {
              type: 'Startup'
              httpGet: {
                path: '/health'
                port: 6000
              }
              failureThreshold: 30
              periodSeconds: 2
            }
          ]
        }
      ]
      ingress: {
        targetPort: 6000
      }
    }
    mcpServerSettings: {
      isMcpServerEnabled: true
    }
    sessionNetworkConfiguration: {
      status: 'egressEnabled'
    }
  }
}

resource scriptPrincipal 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = if (useManagedIdentity){
  name: 'deployScriptIdentity-${suffix}'
  location: location
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (useManagedIdentity) {
  name: guid(scriptPrincipal!.id, 'apps-sessionpool-contributor')
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'f7669afb-68b2-44b4-9c5f-6d2a47fddda0') // Container Apps SessionPools Contributor
    principalId: scriptPrincipal!.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource deployScript 'Microsoft.Resources/deploymentScripts@2020-10-01' = {
  name: 'getmcpkey-${suffix}'
  location: location
  kind: 'AzureCLI'
  identity: useManagedIdentity ? {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${scriptPrincipal!.id}': {}
    }
  } : null
  properties: {
    azCliVersion: '2.77.0'
    scriptContent: '''
      az rest --method post --url "$SESSION_POOL_ID/fetchMCPServerCredentials?api-version=2025-02-02-preview" | jq -c '{"key": .apiKey}' > $AZ_SCRIPTS_OUTPUT_PATH
    '''
    timeout: 'PT30M'
    retentionInterval: 'P1D'
    cleanupPreference: 'OnSuccess'
    environmentVariables: [
      {
        name: 'SESSION_POOL_ID'
        value: sessionPool.id
      }
    ]
  }
}

resource aiAccount 'Microsoft.CognitiveServices/accounts@2025-10-01-preview' = {
  name: 'aia-${suffix}'
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: 'myaiaccount-${suffix}'
    allowProjectManagement: true
  }

  resource project 'projects' = {
    name: 'aip-${suffix}s'
    properties: {
      description: 'This is my AI project.'
    }

    resource mcpConn 'connections' = {
      name: 'aic-${suffix}'
      properties: {
        authType: 'CustomKeys'
        category: 'RemoteTool'
        credentials: {
          keys: {
            'x-ms-apikey': deployScript.properties.outputs.key
          }
        }
        target: sessionPool.properties.mcpServerSettings.mcpServerEndpoint
      }
    }
  }

  resource model 'deployments' = {
    name: modelDeploymentName
    sku: {
      name: 'GlobalStandard'
      capacity: 1
    }
    properties: {
      model: {
        format: 'OpenAI'
        name: modelName
      }
    }
  }
}

@description('Outputs the ID of the project connection for the Code Interpreter MCP Tool')
output AZURE_AI_CONNECTION_ID string = aiAccount::project::mcpConn.id

@description('Model deployment name')
output AZURE_AI_MODEL_DEPLOYMENT_NAME string = aiAccount::model.name

@description('AI Project Endpoint')
output AZURE_AI_PROJECT_ENDPOINT string = aiAccount::project.properties.endpoints['AI Foundry API']
