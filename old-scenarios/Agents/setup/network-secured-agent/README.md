---
description: This set of templates demonstrates how to set up Azure AI Agent Service with virtual network isolation using User Managed Identity authetication for the AI Service/AOAI connection and private network links to connect the agent to your secure data.
page_type: sample
products:
- azure
- azure-resource-manager
urlFragment: network-secured-agent
languages:
- bicep
- json
---

# Network-Secured Azure AI Agent Infrastructure with User Managed Identity

![Azure Public Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/PublicLastTestDate.svg)
![Azure Public Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/PublicDeployment.svg)

![Azure US Gov Last Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/FairfaxLastTestDate.svg)
![Azure US Gov Last Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/FairfaxDeployment.svg)

![Best Practice Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/BestPracticeResult.svg)
![Cred Scan Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/CredScanResult.svg)

![Bicep Version](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.azure-ai-agent-service/network-secured-agent/BicepVersion.svg)

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fnetwork-secured-agent%2Fazuredeploy.json)

[![Visualize](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/visualizebutton.svg?sanitize=true)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fnetwork-secured-agent%2Fazuredeploy.json)

This infrastructure-as-code (IaC) solution deploys a network-secured Azure AI agent environment with private networking, managed identities, and role-based access control (RBAC).


## Note:
Make sure you have an active Azure subscription that allows registering resource providers.
Subnet delegation requires the Microsoft.App provider to be registered in your subscription. If it's not already registered, run the command below:

```
Register-AzResourceProvider -ProviderNamespace Microsoft.App
```

In case Hub/Project workspace need Public Network Disabled select from dropdown or edit in bicep.

```
hubPublicNetworkAccess = Disabled
```

When Hub and Project workspace Public Network Disabled, the project connection string output from the deployment will look like, this should be used data plane operations

```
PROJECT_CONNECTION_STRING='<project_workspace_id>.workspace.japaneast.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name'
```

It follows format
```<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>```
HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery"
To find your discovery_url, run the CLI command:
```az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url```
Customer needs to login to Azure subscription via Azure CLI and set the environment variables


## Architecture Overview

### Network Security Design

The deployment creates an isolated network environment:

- **Virtual Network (172.16.0.0/16)**
  - Customer Hub Subnet (172.16.0.0/24): Hosts private endpoints
  - Agents Subnet (172.16.101.0/24): For azure ai agent workloads

- **Private Endpoints**
  - AI Services
  - AI Search
  - Key Vault
  - Storage Account

- **Private DNS Zones**
  - privatelink.azureml.ms
  - privatelink.search.windows.net
  - privatelink.blob.core.windows.net

### Core Components

1. **AI Hub**
   - Central orchestration point
   - Manages service connections
   - Network-isolated capability hosts

2. **AI Project**
   - Workspace configuration
   - Service integration
   - Agent deployment

3. **Supporting Services**
   - Azure AI Services
   - Azure AI Search
   - Key Vault
   - Storage Account

## Security Features

### Authentication & Authorization

- **Managed Identity**
  - Zero-trust security model
  - No credential storage
  - Platform-managed rotation

- **Role Assignments**
  - AI Services: Administrator, OpenAI User
  - AI Search: Index Data Contributor, Service Contributor
  - Key Vault: Contributor, Secrets Officer
  - Storage: Blob Data Owner, Queue Data Contributor

### Network Security

- Public network access disabled
- Private endpoints for all services
- Service endpoints for Azure services
- Network ACLs with deny by default

## Deployment Options

### 1. Infrastructure as Code (Bicep)
```bash
az deployment group create \
    --template-file main.bicep \
    --parameters @parameters.json
```
Features:
- Declarative approach
- Native Azure integration
- Easy to version control
- Clear resource dependencies

## Module Structure

```
modules-network-secured/
├── ai-search-role-assignments.bicep    # AI Search RBAC configuration
├── ai-search-service.bicep             # AI Search deployment
├── ai-service-role-assignments.bicep   # AI Services RBAC configuration
├── cognitive-services-role-assignments.bicep # OpenAI permissions
├── keyvault-role-assignments.bicep     # Key Vault RBAC configuration
├── network-secured-ai-hub.bicep        # AI Hub deployment
├── network-secured-ai-project.bicep    # AI Project deployment
├── network-secured-dependent-resources.bicep # Core infrastructure
├── network-secured-identity.bicep      # Managed identity
├── private-endpoint-and-dns.bicep      # Network security
└── storage-role-assignments.bicep      # Storage RBAC configuration
```

## Role Assignments

The deployment configures the following RBAC permissions:

### AI Services
- Azure AI Administrator (b78c5d69-af96-48a3-bf8d-a8b4d589de94)
  * Full access to manage AI resources
  * Model deployment permissions
  * Security settings management

### AI Search
- Search Index Data Contributor (8ebe5a00-799e-43f5-93ac-243d3dce84a7)
  * Read/write access to indexes
  * Query and update operations
- Search Service Contributor (7ca78c08-252a-4471-8644-bb5ff32d4ba0)
  * Service management access
  * Configuration changes

### Key Vault
- Key Vault Contributor (f25e0fa2-a7c8-4377-a976-54943a77a395)
  * Manage vault properties
  * Cannot access secrets
- Key Vault Secrets Officer (b86a8fe4-44ce-4948-aee5-eccb2c155cd7)
  * Full secrets access
  * Manage secret metadata

### Storage
- Storage Blob Data Owner (b7e6dc6d-f1e8-4753-8033-0f276bb0955b)
  * Full blob access
  * Container management
- Storage Queue Data Contributor (974c5e8b-45b9-4653-ba55-5f855dd0fb88)
  * Queue operations
  * Message management

## Networking Details

### Private Endpoints
Each service is deployed with a private endpoint in the Customer Hub subnet:

```plaintext
AI Services: account
AI Search: searchService
Storage: blob
```

### DNS Configuration
Private DNS zones are created and linked to the VNet:

```plaintext
AI Services: privatelink.azureml.ms
AI Search: privatelink.search.windows.net
Storage: privatelink.blob.core.windows.net
```

## Security Considerations

1. **Network Isolation**
   - No public internet exposure
   - Private endpoint access only
   - Network ACLs with deny-by-default

2. **Authentication**
   - Managed identity authentication
   - No stored credentials
   - AAD integration

3. **Authorization**
   - Granular RBAC assignments
   - Principle of least privilege
   - Service-specific roles

4. **Monitoring**
   - Diagnostic settings enabled
   - Activity logging
   - Network monitoring

## Limitations
- AI Services/Azure OpenAI resource must be in the same region as Hub and Project workspace. This restriction would be removed in next revision (coming soon).
- The capability host sub-resources of Hub/Project must be deleted before deleting the Hub/Project resource itself. You can use the script as sample to delete it or can be done in alternate ways via ARM. This restriction would be removed in next revision (coming soon).
    - [Run delete script](../utils/deleteCaphost.sh)


## Maintenance

### Regular Tasks
1. Review role assignments
2. Monitor network security
3. Check service health
4. Update configurations as needed

### Troubleshooting
1. Verify private endpoint connectivity
2. Check DNS resolution
3. Validate role assignments
4. Review network security groups

## References

- [Azure AI Services Documentation](https://learn.microsoft.com/en-us/azure/ai-services/)
- [Private Endpoint Documentation](https://learn.microsoft.com/en-us/azure/private-link/)
- [RBAC Documentation](https://learn.microsoft.com/en-us/azure/role-based-access-control/)
- [Network Security Best Practices](https://learn.microsoft.com/en-us/azure/security/fundamentals/network-best-practices)

`Tags: `