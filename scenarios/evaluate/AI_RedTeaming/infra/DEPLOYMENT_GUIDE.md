# Azure AI Red Teaming Infrastructure - Complete Deployment Guide

## 🎯 Overview

This Azure Developer CLI (azd) template provides a complete infrastructure solution for AI Red Teaming scenarios using the Azure AI Evaluation SDK. It deploys a simplified but complete Azure AI Foundry setup with proper authentication and RBAC permissions.

## 🏗️ What Gets Deployed

### Core Azure Resources
- **Azure AI Foundry Account** - AI services account with project management capabilities
- **Azure AI Foundry Project** - Dedicated workspace for red teaming activities  
- **OpenAI Model Deployment** - Single GPT-4o model deployment for cost efficiency
- **Azure Storage Account** - Secure storage for artifacts, logs, and evaluation data
- **Azure AI Search** - Enhanced search capabilities for data retrieval
- **Azure Key Vault** - Secure secret and credential management
- **Log Analytics & Application Insights** - Comprehensive monitoring and logging

### Authentication & Security
- **Managed Identity Configuration** - Seamless service-to-service authentication
- **Role-Based Access Control (RBAC)** - Least-privilege access to all resources
- **DefaultAzureCredential Support** - Multiple authentication methods supported
- **Optional Permission Assignment** - User permissions (disabled by default for deployment reliability)

## 🚀 Quick Start (3 minutes)

### Option 1: Automated Deployment Script (Recommended)
```powershell
# Navigate to the AI_RedTeaming directory (not infra subdirectory)
cd scenarios/evaluate/AI_RedTeaming

# Run the deployment script
.\infra\deploy.ps1
```

### Option 2: Manual Azure Developer CLI
```bash
# Navigate to the AI_RedTeaming directory (not infra subdirectory)
cd scenarios/evaluate/AI_RedTeaming

# Login to Azure
azd auth login

# Deploy infrastructure
azd up
```

**Important**: Run azd commands from the `AI_RedTeaming` directory, not the `infra` subdirectory, since the `azure.yaml` file is located there.

### Option 3: GitHub Actions (CI/CD)
1. Fork this repository
2. Set up GitHub repository secrets (see CI/CD section below)
3. Go to Actions → "Deploy AI Red Teaming Infrastructure" → Run workflow

## 📋 Prerequisites

### Required Tools
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) - Version 1.5.0 or later
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) - Version 2.50.0 or later (optional, for advanced scenarios)
- PowerShell 7+ (for deployment script)

### Azure Requirements
- Azure subscription with **Contributor** permissions
- Ability to create resources in your chosen region
- Sufficient quota for OpenAI services (GPT-4o model)

### Required Permissions for Red Team Operations
The deployment will assign the following roles to enable red team operations:
- **Cognitive Services Contributor** - Required for `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write` permission
- **Cognitive Services OpenAI User** - For accessing OpenAI models
- **Storage Blob Data Contributor** - For managing evaluation data
- **Key Vault Secrets User** - For accessing stored credentials

These permissions are automatically assigned when `createRoleAssignments` is enabled during deployment.

**Important**: If you encounter a `ClientAuthenticationError` with message about lacking `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write` permission, re-run the deployment with role assignments enabled:

```bash
# Re-deploy with role assignments
.\infra\deploy.ps1 -PrincipalId $(az ad signed-in-user show --query "id" -o tsv)
```

### Verifying Your Permissions
Before deployment, verify you have the required permissions:

#### Method 1: Using Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Subscriptions** → Select your subscription
3. Click **Access control (IAM)** → **Role assignments**
4. Search for your email to verify you have **Contributor** role

#### Method 2: Using Azure CLI
```bash
# Check current subscription and account
az account show

# List your role assignments
az role assignment list --assignee $(az account show --query user.name -o tsv) --scope "/subscriptions/$(az account show --query id -o tsv)" --query "[].{Role:roleDefinitionName, Scope:scope}" -o table

# Switch subscription if needed
az account set --subscription <subscription-id>
```

#### Method 3: Test Deployment (Recommended)
The simplest way is to try the deployment - it will fail quickly if you lack permissions:
```bash
# Navigate to AI_RedTeaming directory
cd scenarios/evaluate/AI_RedTeaming

# Try deployment - will fail fast if permissions are insufficient
azd up
```

### Python Environment (for testing)
```bash
pip install azure-ai-evaluation azure-ai-projects azure-storage-blob openai azure-identity
```

## ⚙️ Configuration Options

### Environment Variables
Set these before deployment to customize the infrastructure:

```bash
# Required
export AZURE_ENV_NAME=""        # Insert your environment name
export AZURE_LOCATION=""        # Insert your Azure region

# Optional (role assignments disabled by default for deployment reliability)
export AZURE_PRINCIPAL_ID=""       # Insert your principal ID to enable user permission assignments
```

### Supported Azure Regions
Primary regions with GPT-4o model availability:
- `eastus2` (default) - Good performance and model availability
- `eastus` - Best overall model availability
- `northcentralus` - Central US option
- `westus2` - West coast option  
- `westus3` - Latest west coast region
- `westeurope` - European option
- `uksouth` - UK option
- `australiaeast` - Asia-Pacific option
- `japaneast` - Asia option

### Model Deployment
The template deploys a single model by default for cost efficiency:
- **GPT-4o** (gpt-4o) - 1 TPM capacity - Latest multimodal model

To customize capacity or add models, edit `main.bicepparam`:
```bicep
# Current default configuration (cost-optimized)
param modelDeployments = [
  {
    name: 'gpt-4o-mini'
    model: { format: 'OpenAI', name: 'gpt-4o-mini', version: '2024-07-18' }
    sku: { name: 'GlobalStandard', capacity: 5 }
  }
]
```

## 🔐 Authentication Setup

### For Local Development
After deployment, authenticate using any of these methods:

```bash
# Option 1: Azure CLI (recommended)
az login

# Option 2: Azure Developer CLI
azd auth login

# Option 3: Azure PowerShell
Connect-AzAccount
```

### For Python Code
The infrastructure is configured to work with `DefaultAzureCredential`:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os

# This will automatically use your logged-in credentials
credential = DefaultAzureCredential()
project_client = AIProjectClient.from_connection_string(
    conn_str=os.environ["AZURE_AI_PROJECT_CONNECTION_STRING"],
    credential=credential
)
```

## 🧪 Testing Your Deployment

### Automated Testing
Run the included test script to verify everything works:

```bash
# Navigate to the infra directory
cd infra

# Set environment variables from deployment output
# (These will be displayed after successful deployment)
export AZURE_AI_PROJECT_CONNECTION_STRING=""
export AZURE_OPENAI_ENDPOINT=""
export AZURE_STORAGE_ACCOUNT_NAME=""

# Run tests
python test_deployment.py
```

### Manual Verification
Check these components individually:

1. **Azure AI Project**: Visit [AI Studio](https://ai.azure.com) and verify your project appears
2. **OpenAI Models**: Test in Azure OpenAI Studio playground
3. **Storage**: Check containers in Azure Storage Explorer
4. **Permissions**: Run `az role assignment list --scope /subscriptions/...` to verify RBAC

## 🔧 Troubleshooting

### Common Issues

#### Authentication Errors
```
DefaultAzureCredential failed to retrieve a token
```
**Solution**: 
```bash
# Clear any cached credentials and re-login
az account clear
az login
azd auth login
```

#### Resource Naming Conflicts
```
The storage account name is already taken
```
**Solution**: Change environment name to generate new unique names:
```bash
azd up --set environmentName="my-unique-name-$(date +%s)"
```

#### Quota Exceeded
```
Deployment failed: Insufficient quota for OpenAI
```
**Solution**: 
1. Check quota in Azure Portal → Cognitive Services → Quotas
2. Request quota increase or try different region
3. Reduce model capacity in `main.bicepparam`

#### Permission Denied
```
The client does not have authorization to perform action
```
**Solution**:
1. Verify you have **Contributor** role on subscription
2. Check subscription with: `az account show`
3. Switch subscription with: `az account set --subscription <subscription-id>`
4. List available subscriptions: `az account list --output table`

#### Role Assignment Issues
```
Role assignments failed during deployment
```
**Solution**:
The template disables role assignments by default for deployment reliability. This is normal and doesn't affect functionality since Azure AI services use managed identities for authentication.

### Getting Help
1. Check deployment logs: `azd show --environment <env-name>`
2. Review Azure Portal → Resource Groups → Activity Log
3. Validate Bicep templates: `az deployment group validate`

## 🏢 CI/CD with GitHub Actions

The repository includes GitHub Actions workflow for automated deployment.

### Setup Steps
1. **Create Service Principal**:
   ```bash
   az ad sp create-for-rbac --name "ai-red-team-deploy" \
     --role contributor \
     --scopes /subscriptions/<subscription-id> \
     --sdk-auth
   ```

2. **Set Repository Secrets**:
   - `AZURE_CREDENTIALS`: Full JSON output from step 1
   - `AZURE_SUBSCRIPTION_ID`: Your subscription ID
   - `AZURE_TENANT_ID`: Your tenant ID

### Workflow Usage
The GitHub Actions workflow is located in `.github/workflows/` and can be triggered manually or on push to main branch.

## 📁 File Structure

```
AI_RedTeaming/
├── azure.yaml                    # Azure Developer CLI configuration
├── AI_RedTeaming.ipynb           # Main red teaming notebook
├── README.md                     # Quick start guide
├── data/                         # Sample data for testing
├── .azure/                       # azd environment data (created during deployment)
└── infra/                        # Infrastructure as Code
    ├── main.bicep                # Main deployment template
    ├── ai-red-team.bicep         # Resource definitions
    ├── main.bicepparam           # Default parameters
    ├── deploy.ps1                # Automated deployment script
    ├── test_deployment.py        # Verification script
    ├── .env.sample               # Environment variables template
    ├── README.md                 # Basic usage instructions
    ├── DEPLOYMENT_GUIDE.md       # This comprehensive guide
    └── .github/
        └── workflows/
            └── deploy.yml         # GitHub Actions workflow
```

## 🧹 Cleanup

### Remove All Resources
```bash
# Navigate to the AI_RedTeaming directory
cd scenarios/evaluate/AI_RedTeaming

# Destroy everything
azd down --environment <your-env-name>

# Force removal and purge Key Vault
azd down --environment <your-env-name> --force --purge
```

### Partial Cleanup
```bash
# Remove specific resource group
az group delete --name <resource-group-name> --yes --no-wait

# Purge soft-deleted Key Vault
az keyvault purge --name <keyvault-name>
```

## 💡 Advanced Customization

### Adding Custom Resources
Edit `ai-red-team.bicep` to add additional resources:

```bicep
// Example: Add Azure Cosmos DB
resource cosmosDb 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: 'cosmos-${resourceToken}'
  location: location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [ { locationName: location, failoverPriority: 0 } ]
  }
}
```

### Custom Model Deployments
Modify the hardcoded model in `ai-red-team.bicep` or add additional deployments:

```bicep
// Current single model deployment
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
  parent: aiFoundry
  name: 'gpt-4o'
  sku : {
    capacity: 1  // Increase capacity if needed
    name: 'GlobalStandard'
  }
  properties: {
    model:{
      name: 'gpt-4o'
      format: 'OpenAI'
    }
  }
}
```

### Environment-Specific Configurations
Create multiple `.bicepparam` files for different environments:

- `dev.bicepparam` - Development settings
- `prod.bicepparam` - Production settings  
- `test.bicepparam` - Testing configurations

### Enabling Role Assignments
To enable automatic role assignments (requires higher permissions):

1. Edit `main.bicepparam`:
```bicep
param principalId = 'your-user-object-id'
```

2. Update the `createRoleAssignments` parameter in `main.bicep`:
```bicep
createRoleAssignments: true
```

## 🎉 Success! What's Next?

After successful deployment:

1. **Copy environment variables** from deployment output (automatically displayed)
2. **Run test script** to verify everything works: `python infra/test_deployment.py`
3. **Start your AI Red Teaming** with the `AI_RedTeaming.ipynb` notebook
4. **Explore Azure AI Studio** to manage your project and models at [ai.azure.com](https://ai.azure.com)
5. **Set up monitoring** using Application Insights dashboards

### Key Resources Created
Your deployment creates these main resources:
- AI Foundry Account: `aifoundry-{token}`
- AI Project: `aiproject-{token}` 
- Storage Account: `st{token}`
- Key Vault: `kv-{token}`
- Search Service: `search-{token}`
- Model Deployment: `gpt-4o` (ready to use)

### Authentication Notes
- The infrastructure uses **managed identities** for service-to-service authentication
- Your user account may need explicit role assignments for full access
- Use `DefaultAzureCredential` in your Python code for seamless authentication

## 📚 Additional Resources

- [Azure AI Evaluation SDK Documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation)
- [Azure AI Studio Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure Developer CLI Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)

---

**Need Help?** Open an issue in the repository or consult the troubleshooting section above.