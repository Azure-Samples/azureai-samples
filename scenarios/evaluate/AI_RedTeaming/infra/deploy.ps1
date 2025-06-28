#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Deploy Azure AI Red Teaming infrastructure using Azure Developer CLI

.DESCRIPTION
    This script simplifies the deployment of Azure AI Red Teaming infrastructure.
    It checks prerequisites, authenticates with Azure, and deploys the resources.

.PARAMETER EnvironmentName
    Name of the environment (default: ai-red-team-dev)

.PARAMETER Location
    Azure region for deployment (default: eastus)

.PARAMETER PrincipalId
    Object ID of user to assign permissions to (optional)

.PARAMETER SkipPrereqs
    Skip prerequisite checks

.EXAMPLE
    .\deploy.ps1
    Deploy with default settings

.EXAMPLE
    .\deploy.ps1 -EnvironmentName "my-red-team" -Location "westus2"
    Deploy with custom environment name and location

.EXAMPLE
    .\deploy.ps1 -PrincipalId "12345678-1234-1234-1234-123456789012"
    Deploy and assign permissions to specific user
#>

param(
    [string]$EnvironmentName = "ai-red-team-dev",
    [string]$Location = "eastus2",
    [string]$PrincipalId = "",
    [switch]$SkipPrereqs = $false
)

# Color functions for better output
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

Write-Host "🚀 Azure AI Red Teaming Infrastructure Deployment" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta

# Check prerequisites
if (-not $SkipPrereqs) {
    Write-Info "Checking prerequisites..."
    
    # Check Azure Developer CLI
    try {
        $azdVersion = azd version 2>$null
        Write-Success "✓ Azure Developer CLI found: $azdVersion"
    }
    catch {
        Write-Error "✗ Azure Developer CLI not found. Please install from: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd"
        exit 1
    }
    
    # Check Azure CLI
    try {
        $azVersion = az version --query '"azure-cli"' -o tsv 2>$null
        Write-Success "✓ Azure CLI found: $azVersion"
    }
    catch {
        Write-Error "✗ Azure CLI not found. Please install from: https://docs.microsoft.com/cli/azure/install-azure-cli"
        exit 1
    }
}

# Check if user is logged in
Write-Info "Checking Azure authentication..."
try {
    $currentUser = az account show --query "user.name" -o tsv 2>$null
    if ($currentUser) {
        Write-Success "✓ Logged in as: $currentUser"
    } else {
        Write-Warning "Not logged in to Azure. Initiating login..."
        azd auth login
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Login failed. Please run 'azd auth login' manually."
            exit 1
        }
    }
}
catch {
    Write-Warning "Could not verify Azure login status. Attempting to login..."
    azd auth login
}

# Check and select Azure subscription
Write-Info "Checking Azure subscription..."
try {
    # Try different approaches to get subscription info
    $currentSub = $null
    
    # First try with azd
    try {
        $azdSub = azd env get-value AZURE_SUBSCRIPTION_ID 2>$null
        if ($azdSub) {
            Write-Info "Found subscription from azd environment: $azdSub"
            $currentSub = @{ name = "From azd environment"; id = $azdSub }
        }
    }
    catch { }
    
    # If azd didn't work, try az CLI
    if (-not $currentSub) {
        try {
            $azSub = az account show --query "{name:name, id:id}" -o json 2>$null
            if ($azSub) {
                $currentSub = $azSub | ConvertFrom-Json
            }
        }
        catch { }
    }
    
    if ($currentSub) {
        Write-Host "Current subscription: $($currentSub.name) ($($currentSub.id))" -ForegroundColor White
        Write-Success "✓ Using subscription: $($currentSub.name)"
        
        # Check if user has sufficient permissions (basic check)
        Write-Info "💡 Make sure you have Contributor permissions on this subscription for deployment to succeed"
    } else {
        Write-Warning "Could not determine current subscription automatically."
        Write-Info "Available options:"
        Write-Host "1. Set subscription with azd: azd env set AZURE_SUBSCRIPTION_ID <subscription-id>" -ForegroundColor White
        Write-Host "2. Set subscription with az CLI: az account set --subscription <subscription-id>" -ForegroundColor White
        Write-Host "3. List subscriptions: az account list --output table" -ForegroundColor White
        Write-Host ""
        
        $manualSub = Read-Host "Enter your Azure subscription ID (or press Enter to continue and let azd handle it)"
        if ($manualSub) {
            Write-Info "Setting subscription: $manualSub"
            azd env set AZURE_SUBSCRIPTION_ID $manualSub
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✓ Subscription set successfully"
            }
        } else {
            Write-Info "Continuing without explicit subscription selection - azd will prompt if needed"
        }
    }
}
catch {
    Write-Warning "Could not verify subscription. Continuing anyway - azd will handle subscription selection."
}

# Principal ID is optional - role assignments are disabled by default
# Check if PrincipalId was passed as parameter or exists in azd environment
if ([string]::IsNullOrEmpty($PrincipalId)) {
    try {
        $existingPrincipalId = azd env get-value AZURE_PRINCIPAL_ID 2>$null
        if ($existingPrincipalId) {
            $PrincipalId = $existingPrincipalId
            Write-Info "Found existing Principal ID in environment: $PrincipalId"
        } else {
            Write-Info "Principal ID not specified - role assignments will be skipped (recommended for most deployments)"
        }
    } catch {
        Write-Info "Principal ID not specified - role assignments will be skipped (recommended for most deployments)"
    }
} else {
    Write-Info "Principal ID provided as parameter: $PrincipalId"
}

# Display deployment configuration
Write-Host ""
Write-Info "Deployment Configuration:"
Write-Host "  Environment Name: $EnvironmentName" -ForegroundColor White
Write-Host "  Location: $Location" -ForegroundColor White
Write-Host "  Principal ID: $(if ($PrincipalId) { $PrincipalId } else { 'Not specified (role assignments disabled)' })" -ForegroundColor White
Write-Host ""

# Confirm deployment
$confirmation = Read-Host "Do you want to proceed with the deployment? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Warning "Deployment cancelled."
    exit 0
}

# Set environment variables for azd
$env:AZURE_ENV_NAME = $EnvironmentName
$env:AZURE_LOCATION = $Location

# Ensure azd environment has the current parameter values
Write-Info "Updating azd environment with current parameters..."
azd env set AZURE_LOCATION $Location
if ($LASTEXITCODE -eq 0) {
    Write-Success "✓ Location set to: $Location"
} else {
    Write-Warning "Could not set location in azd environment, continuing anyway..."
}

# Get current user's principal ID if not provided for red team operations
if (-not $PrincipalId) {
    Write-Info "Getting current user's principal ID for role assignments..."
    try {
        $PrincipalId = az ad signed-in-user show --query "id" -o tsv 2>$null
        if ($PrincipalId) {
            Write-Success "✓ Found current user principal ID: $PrincipalId"
        } else {
            Write-Warning "Could not get current user principal ID. Role assignments will be disabled."
        }
    }
    catch {
        Write-Warning "Could not get current user principal ID. Role assignments will be disabled."
    }
}

# Set principal ID and enable role assignments for red team operations
if ($PrincipalId) {
    $env:AZURE_PRINCIPAL_ID = $PrincipalId
    azd env set AZURE_PRINCIPAL_ID $PrincipalId
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✓ Principal ID set: $PrincipalId - role assignments will be enabled"
        Write-Info "  This enables required permissions for red team evaluation operations"
    } else {
        Write-Warning "Could not set Principal ID in azd environment, continuing anyway..."
    }
} else {
    Write-Warning "No Principal ID available - role assignments will be disabled"
    Write-Warning "You may need to manually assign permissions after deployment"
}

# Ensure we're using the correct subscription
try {
    $currentSubId = azd env get-value AZURE_SUBSCRIPTION_ID 2>$null
    if (-not $currentSubId) {
        $currentSubId = az account show --query "id" -o tsv 2>$null
    }
    if ($currentSubId) {
        Write-Info "Using subscription: $currentSubId"
    } else {
        Write-Info "Subscription will be selected during deployment"
    }
}
catch {
    Write-Info "Subscription will be selected during deployment"
}

# Initialize azd environment if needed
Write-Info "Initializing Azure Developer CLI environment..."
if (-not (Test-Path ".azure")) {
    azd init --environment $EnvironmentName --no-prompt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to initialize azd environment."
        exit 1
    }
}

# Deploy infrastructure
Write-Info "Starting infrastructure deployment..."
Write-Host "This may take 10-15 minutes to complete..." -ForegroundColor Yellow
Write-Host ""
Write-Info "💡 If you encounter permission errors:"
Write-Host "   1. Make sure you're using a subscription where you have Contributor permissions" -ForegroundColor White
Write-Host "   2. You can switch subscriptions with: az account set --subscription <subscription-id>" -ForegroundColor White
Write-Host "   3. List available subscriptions with: az account list --output table" -ForegroundColor White
Write-Host ""

azd up --environment $EnvironmentName --no-prompt
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Deployment failed!"
    Write-Host ""    Write-Warning "🔧 Troubleshooting steps:"
    Write-Host "1. Check that you're using the correct Azure subscription" -ForegroundColor White
    Write-Host "2. Verify you have Contributor permissions on the subscription" -ForegroundColor White
    Write-Host "3. Try using a different environment name if resources already exist" -ForegroundColor White
    Write-Host "4. Run 'azd env list' to see existing environments" -ForegroundColor White
    Write-Host "5. List subscriptions with: az account list --output table" -ForegroundColor White
    Write-Host "6. Switch subscription with: az account set --subscription <subscription-id>" -ForegroundColor White
    exit 1
}

Write-Success "🎉 Deployment completed successfully!"
Write-Host ""

# Create .env file with deployment outputs
Write-Info "Creating .env file with deployment outputs..."
$envFilePath = Join-Path (Get-Location) ".env"
try {
    $envVars = azd env get-values
    if ($LASTEXITCODE -eq 0 -and $envVars) {
        # Parse environment variables into a hashtable
        $envHash = @{}
        $envVars | ForEach-Object {
            if ($_ -match '^([^=]+)=(.*)$') {
                $varName = $Matches[1]
                $varValue = $Matches[2].Trim('"')
                $envHash[$varName] = $varValue
            }        }
          # Create the correct Azure AI Foundry project endpoint format
        # Format: https://{foundry-name}.services.ai.azure.com/api/projects/{project-name}
        if ($envHash.ContainsKey('AI_FOUNDRY_NAME') -and 
            $envHash.ContainsKey('AI_PROJECT_NAME')) {
            
            $projectEndpoint = "https://$($envHash['AI_FOUNDRY_NAME']).services.ai.azure.com/api/projects/$($envHash['AI_PROJECT_NAME'])"
            $envHash['AZURE_AI_PROJECT_ENDPOINT'] = $projectEndpoint
            Write-Info "✓ Generated Azure AI Foundry project endpoint"
        }
        
        # Ensure all required variables are present for the test script
        if ($envHash.ContainsKey('AI_FOUNDRY_ENDPOINT')) {
            # Keep the foundry endpoint for the test script
            Write-Info "✓ AI Foundry endpoint available"
        }
        
        # Ensure we have the resource group name  
        if (-not $envHash.ContainsKey('AZURE_RESOURCE_GROUP') -and $envHash.ContainsKey('AZURE_RESOURCE_GROUP_NAME')) {
            $envHash['AZURE_RESOURCE_GROUP'] = $envHash['AZURE_RESOURCE_GROUP_NAME']
        }
        
        # Write corrected environment variables to .env file
        $envContent = @()
        $envHash.GetEnumerator() | Sort-Object Name | ForEach-Object {
            $envContent += "$($_.Key)=`"$($_.Value)`""
        }
        $envContent | Out-File -FilePath $envFilePath -Encoding UTF8
        Write-Success "✓ Created .env file: $envFilePath"
          # Display key environment variables
        Write-Host ""
        Write-Info "Key environment variables:"
        Write-Host "  AZURE_SUBSCRIPTION_ID=`"$($envHash['AZURE_SUBSCRIPTION_ID'])`"" -ForegroundColor White
        Write-Host "  AZURE_RESOURCE_GROUP=`"$($envHash['AZURE_RESOURCE_GROUP'])`"" -ForegroundColor White  
        Write-Host "  AI_PROJECT_NAME=`"$($envHash['AI_PROJECT_NAME'])`"" -ForegroundColor White
        Write-Host "  AI_FOUNDRY_ENDPOINT=`"$($envHash['AI_FOUNDRY_ENDPOINT'])`"" -ForegroundColor White
        Write-Host "  AZURE_OPENAI_ENDPOINT=`"$($envHash['AZURE_OPENAI_ENDPOINT'])`"" -ForegroundColor White
        Write-Host "  AZURE_STORAGE_ACCOUNT_NAME=`"$($envHash['AZURE_STORAGE_ACCOUNT_NAME'])`"" -ForegroundColor White
    } else {
        Write-Warning "Could not retrieve environment variables from azd"
    }
}
catch {
    Write-Warning "Failed to create .env file: $($_.Exception.Message)"
}

# Run deployment test
Write-Host ""
Write-Info "Running deployment verification test..."
$testScript = Join-Path $PSScriptRoot "test_deployment.py"
if (Test-Path $testScript) {
    try {
        # Check if python is available
        $pythonCmd = $null
        foreach ($cmd in @("python", "python3", "py")) {
            try {
                $version = & $cmd --version 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $pythonCmd = $cmd
                    Write-Info "Using Python: $version"
                    break
                }
            }
            catch { }
        }
        
        if ($pythonCmd) {
            Write-Host ""            Write-Info "🧪 Testing deployment..."
            # Set environment variables for the test using corrected values
            $envVars = azd env get-values
            if ($envVars) {
                # Parse and set environment variables with corrections
                $envHash = @{}
                $envVars | ForEach-Object {
                    if ($_ -match '^([^=]+)=(.*)$') {
                        $varName = $Matches[1]
                        $varValue = $Matches[2].Trim('"')
                        $envHash[$varName] = $varValue
                    }
                }                  # Apply the Azure AI Foundry project endpoint
                if ($envHash.ContainsKey('AI_FOUNDRY_NAME') -and 
                    $envHash.ContainsKey('AI_PROJECT_NAME')) {
                    
                    $projectEndpoint = "https://$($envHash['AI_FOUNDRY_NAME']).services.ai.azure.com/api/projects/$($envHash['AI_PROJECT_NAME'])"
                    $envHash['AZURE_AI_PROJECT_ENDPOINT'] = $projectEndpoint
                }
                
                # Ensure we have the resource group name
                if (-not $envHash.ContainsKey('AZURE_RESOURCE_GROUP') -and $envHash.ContainsKey('AZURE_RESOURCE_GROUP_NAME')) {
                    $envHash['AZURE_RESOURCE_GROUP'] = $envHash['AZURE_RESOURCE_GROUP_NAME']
                }
                
                # Set all environment variables
                $envHash.GetEnumerator() | ForEach-Object {
                    Set-Item -Path "env:$($_.Key)" -Value $_.Value
                }
            }
            
            & $pythonCmd $testScript
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✓ Deployment test passed!"
            } else {
                Write-Warning "⚠ Deployment test had issues. Check the output above."
            }
        } else {
            Write-Warning "Python not found. Please install Python to run deployment tests."
            Write-Info "You can manually run: python infra/test_deployment.py"
        }
    }
    catch {
        Write-Warning "Error running deployment test: $($_.Exception.Message)"
    }
} else {
    Write-Warning "Test script not found at: $testScript"
}

Write-Host ""
Write-Success "Next steps:"
Write-Host "1. ✓ Environment variables are saved in .env file" -ForegroundColor White
Write-Host "2. ✓ Deployment has been tested" -ForegroundColor White
Write-Host "3. Run your AI Red Teaming notebooks or scripts" -ForegroundColor White
Write-Host ""
Write-Info "To clean up resources later, run: azd down --environment $EnvironmentName"