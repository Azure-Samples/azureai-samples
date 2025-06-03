# Azure Developer CLI Template for AI Red Teaming

This template provides the necessary Azure infrastructure for running AI Red Teaming scenarios using the Azure AI Evaluation SDK. It deploys a simplified Azure AI Foundry setup with proper authentication and permissions configured for red team operations.

## Prerequisites

- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- PowerShell 7+ (for the deployment script)
- An Azure subscription with Contributor permissions

## Quick Start

1. **Clone and navigate to this directory**
   ```bash
   cd scenarios/evaluate/AI_RedTeaming/
   ```

2. **Run the deployment script (recommended)**
   ```bash
   .\deploy.ps1
   ```
   
   The script will:
   - Check prerequisites and authenticate with Azure
   - Automatically detect your user principal ID for permissions
   - Deploy all required Azure resources
   - Configure RBAC permissions for red team operations
   - Output environment variables for your `.env` file

3. **Alternative: Manual deployment with azd**
   ```bash
   # Login to Azure
   azd auth login
   
   # Initialize and deploy
   azd init
   azd up
   ```

4. **Set up your environment variables**
   - Copy the output from the deployment
   - Create a `.env` file in the parent directory (`AI_RedTeaming/.env`)
   - The variables follow this format:
     ```
     azure_ai_project="https://your-foundry.services.ai.azure.com/api/projects/your-project"
     azure_openai_config='{"endpoint": "...", "api_key": "...", "deployment": "gpt-4o", "api_version": "2024-10-21"}'
     azure_storage_account="your-storage-account-name"
     ```

## What Gets Deployed

This template creates the following Azure resources:

- **Azure AI Foundry Account** - Simplified AI services account with built-in OpenAI capabilities
- **Azure AI Foundry Project** - Project workspace for red teaming operations
- **GPT-4o Model Deployment** - Single cost-optimized model deployment
- **Azure Storage Account** - For storing evaluation artifacts and data
- **Azure AI Search** - For enhanced search capabilities (basic tier)
- **Azure Key Vault** - For secure secret management
- **Log Analytics & Application Insights** - For monitoring and logging

## Authentication & Permissions

The template automatically configures:

- **Role-Based Access Control (RBAC)** for all services
- **Managed Identity** permissions for Azure AI services
- **User permissions** for your account (automatically detected during deployment)
- **DefaultAzureCredential** support for seamless authentication

Required roles assigned for red team operations:
- `Cognitive Services Contributor` - **Required for red team evaluations** (provides `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write` permission)
- `Cognitive Services OpenAI User` - For OpenAI model access
- `Storage Blob Data Contributor` - For storage access and evaluation data
- `Search Index Data Contributor` - For search access
- `Key Vault Secrets User` - For Key Vault access

**Note:** The deployment script automatically detects your user principal ID and assigns the necessary permissions for red team operations.

## Configuration Options

You can customize the deployment:

**Using the deployment script (recommended):**
```bash
# Deploy to a specific location
.\deploy.ps1 -Location "westus2"

# Use custom environment name
.\deploy.ps1 -EnvironmentName "my-red-team-env"

# Specify user principal ID manually
.\deploy.ps1 -PrincipalId "your-user-object-id"
```

**Using azd directly:**
```bash
# Deploy to a specific location
azd up --set location=westus2

# Assign permissions to specific user
azd up --set principalId=your-user-object-id
```

**Supported Azure regions with GPT-4o and RedTeam availability:**
- `eastus2` (default)
- `swedencentral`

## Environment Variables

After deployment, use these environment variables in your Python code:

```python
import os
import json
from dotenv import load_dotenv
from azure.ai.evaluation.red_team import RedTeam
from azure.identity import DefaultAzureCredential

# Load environment variables from .env file
load_dotenv()

# Initialize credential
credential = DefaultAzureCredential()

# Get configuration from deployment outputs
azure_ai_project = os.environ.get("azure_ai_project")
azure_openai_config = json.loads(os.environ.get("azure_openai_config"))

# Initialize RedTeam for evaluation
red_team = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=credential
)
```

## Troubleshooting

### Red Team Permission Errors

If you encounter the error `Microsoft.CognitiveServices/accounts/AIServices/evaluations/write`:

1. **Redeploy with proper permissions:**
   ```bash
   .\deploy.ps1
   ```
   The script automatically assigns the required `Cognitive Services Contributor` role.

2. **Manual permission assignment:**
   ```bash
   # Get your user object ID
   az ad signed-in-user show --query "id" -o tsv
   
   # Deploy with explicit principal ID
   .\deploy.ps1 -PrincipalId <your-object-id>
   ```

3. **Verify permissions in Azure Portal:**
   - Navigate to your AI Foundry resource
   - Check **Access control (IAM)** → **Role assignments**
   - Ensure you have `Cognitive Services Contributor` role

### Authentication Issues

If you encounter authentication errors:

1. Ensure you're logged in: `az login` or `azd auth login`
2. Check your permissions in the Azure portal
3. Verify the environment variables are set correctly
4. Try `az account show` to confirm your active subscription

### Resource Deployment Failures

Common issues:
- **Quota limits**: Check OpenAI and other service quotas in your region
- **Naming conflicts**: Resource names must be globally unique
- **Permissions**: Ensure you have Contributor access to the subscription

### Testing Your Deployment

Run the test script to verify everything is working:
```bash
python test_deployment.py
```

## Clean Up

To remove all deployed resources:

```bash
azd down
```

This will delete the resource group and all contained resources.

## Support

For issues with:
- **Azure Developer CLI**: Visit [azd documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- **Azure AI Evaluation SDK**: Check the [SDK documentation](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation)
- **Azure AI Foundry**: See [Azure AI Studio documentation](https://learn.microsoft.com/azure/ai-studio/)
