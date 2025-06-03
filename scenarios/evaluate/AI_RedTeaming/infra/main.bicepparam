using 'main.bicep'

// Environment configuration
param environmentName = readEnvironmentVariable('AZURE_ENV_NAME', 'ai-red-team-dev')
param location = readEnvironmentVariable('AZURE_LOCATION', 'eastus2')

// User permissions (optional - set via azd up --set principalId=<your-user-id>)
// Leave empty for now to skip role assignments due to permission issues
param principalId = readEnvironmentVariable('AZURE_PRINCIPAL_ID', '')