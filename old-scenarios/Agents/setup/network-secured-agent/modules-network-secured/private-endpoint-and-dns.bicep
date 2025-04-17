/*
Private Endpoint and DNS Configuration Module
------------------------------------------
This module configures private network access for Azure services using:

1. Private Endpoints:
   - Creates network interfaces in the specified subnet
   - Establishes private connections to Azure services
   - Enables secure access without public internet exposure

2. Private DNS Zones:
   - privatelink.azureml.ms for AI Services
   - privatelink.search.windows.net for AI Search
   - privatelink.blob.core.windows.net for Storage
   - Enables custom DNS resolution for private endpoints

3. DNS Zone Links:
   - Links private DNS zones to the VNet
   - Enables name resolution for resources in the VNet
   - Prevents DNS resolution conflicts

Security Benefits:
- Eliminates public internet exposure
- Enables secure access from within VNet
- Prevents data exfiltration through network
*/

// Resource names and identifiers
@description('Name of the AI Services account')
param aiServicesName string
@description('Name of the AI Search service')
param aiSearchName string
@description('Name of the storage account')
param storageName string
@description('Name of the Vnet')
param vnetName string
@description('Name of the Customer subnet')
param cxSubnetName string
@description('Suffix for unique resource names')
param suffix string
@description('Name of the AI Storage Account')
param aiStorageId string

@description('Specifies the resource id of the Azure Hub Workspace.')
param hubWorkspaceId string

@description('Name of the Customer Hub Workspace')
@secure()
param hubWorkspaceName string

// Reference existing services that need private endpoints
resource aiServices 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: aiServicesName
  scope: resourceGroup()
}

resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' existing = {
  name: aiSearchName
  scope: resourceGroup()
}

// Reference existing network resources
resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name: vnetName
  scope: resourceGroup()
}

resource cxSubnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' existing = {
  parent: vnet
  name: cxSubnetName
}

/* -------------------------------------------- AI Services Private Endpoint -------------------------------------------- */

// Private endpoint for AI Services
// - Creates network interface in customer hub subnet
// - Establishes private connection to AI Services account
resource aiServicesPrivateEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: '${aiServicesName}-private-endpoint'
  location: resourceGroup().location
  properties: {
    subnet: {
      id: cxSubnet.id                    // Deploy in customer hub subnet
    }
    privateLinkServiceConnections: [
      {
        name: '${aiServicesName}-private-link-service-connection'
        properties: {
          privateLinkServiceId: aiServices.id
          groupIds: [
            'account'                     // Target AI Services account
          ]
        }
      }
    ]
  }
}

resource aiServiceOpenAiPrivateEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: '${aiServicesName}-openAi-private-endpoint'
  location: resourceGroup().location
  properties: {
    subnet: {
      id: cxSubnet.id                    // Deploy in customer hub subnet
    }
    privateLinkServiceConnections: [
      {
        name: '${aiServicesName}-openAi-private-link-service-connection'
        properties: {
          privateLinkServiceId: aiServices.id
          groupIds: [
            'account'                     // Target AI Services account
          ]
        }
      }
    ]
  }
}

/* -------------------------------------------- AI Search Private Endpoint -------------------------------------------- */

// Private endpoint for AI Search
// - Creates network interface in customer hub subnet
// - Establishes private connection to AI Search service
resource aiSearchPrivateEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: '${aiSearchName}-private-endpoint'
  location: resourceGroup().location
  properties: {
    subnet: {
      id: cxSubnet.id                    // Deploy in customer hub subnet
    }
    privateLinkServiceConnections: [
      {
        name: '${aiSearchName}-private-link-service-connection'
        properties: {
          privateLinkServiceId: aiSearch.id
          groupIds: [
            'searchService'               // Target search service
          ]
        }
      }
    ]
  }
}

/* -------------------------------------------- Storage Private Endpoint -------------------------------------------- */

// Private endpoint for Storage Account
// - Creates network interface in customer hub subnet
// - Establishes private connection to blob storage
resource storagePrivateEndpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: '${storageName}-private-endpoint'
  location: resourceGroup().location
  properties: {
    subnet: {
      id: cxSubnet.id                    // Deploy in customer hub subnet
    }
    privateLinkServiceConnections: [
      {
        name: '${storageName}-private-link-service-connection'
        properties: {
          privateLinkServiceId: aiStorageId
          groupIds: [
            'blob'                        // Target blob storage
          ]
        }
      }
    ]
  }
}

/*----------------------------------------------Hub Workspace Kind---------------------------------------------*/
resource hubWorkspacePrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-11-01' = {
  name: '${hubWorkspaceName}-private-endpoint'
  location: resourceGroup().location
  properties: {
    privateLinkServiceConnections: [
      {
        name: '${hubWorkspaceName}-private-link-service-connection'
        properties: {
          privateLinkServiceId: hubWorkspaceId
          groupIds: [
            'amlworkspace'
          ]
        }
      }
    ]
    subnet: {
      id: cxSubnet.id
    }
  }
}

/* -------------------------------------------- Private DNS Zones -------------------------------------------- */

// Private DNS Zone for AI Services
// - Enables custom DNS resolution for AI Services private endpoint
resource aiServicesPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.azureml.ms'         // Standard DNS zone for AI Services
  location: 'global'
}

resource openAiPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.openai.azure.com'
  location: 'global'
}

// Link AI Services DNS Zone to VNet
resource aiServicesLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  parent: aiServicesPrivateDnsZone
  location: 'global'
  name: 'aiServices-${suffix}-link'
  properties: {
    virtualNetwork: {
      id: vnet.id                        // Link to specified VNet
    }
    registrationEnabled: false           // Don't auto-register VNet resources
  }
}

resource aiOpenAILink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  parent: openAiPrivateDnsZone
  location: 'global'
  name: 'aiServicesOpenAI-${suffix}-link'
  properties: {
    virtualNetwork: {
      id: vnet.id                        // Link to specified VNet
    }
    registrationEnabled: false           // Don't auto-register VNet resources
  }
}

// DNS Zone Group for AI Services
resource aiServicesDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: aiServicesPrivateEndpoint
  name: '${aiServicesName}-dns-group'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${aiServicesName}-dns-config'
        properties: {
          privateDnsZoneId: aiServicesPrivateDnsZone.id
        }
      }
    ]
  }
  dependsOn: [
    aiServicesLink
  ]
}

// DNS Zone Group for Azure OpenAI
resource aiOpenAIDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: aiServiceOpenAiPrivateEndpoint
  name: '${aiServicesName}-openAi-dns-group'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${aiServicesName}-openAi-dns-config'
        properties: {
          privateDnsZoneId: openAiPrivateDnsZone.id
        }
      }
    ]
  }
  dependsOn: [
    aiOpenAILink
  ]
}

// Private DNS Zone for AI Hub
// - Enables custom DNS resolution for AI Hub private endpoint
resource mlApiPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.api.azureml.ms'
  location: 'global'
}

resource mlNotebooksPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.notebooksazureml.net'
  location: 'global'
}

// Link AI Hub DNS Zone to VNet
resource mlApiPrivateDnsZoneVirtualNetworkLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: mlApiPrivateDnsZone
  name: 'mlApi-${suffix}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: vnet.id
    }
  }
}

resource mlNotebooksPrivateDnsZoneVirtualNetworkLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: mlNotebooksPrivateDnsZone
  name: 'mlNotebook-${suffix}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: vnet.id
    }
  }
}

resource hubWorkspacePrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  parent: hubWorkspacePrivateEndpoint
  name: '${hubWorkspaceName}-mlApiNotebook-dns-group'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${hubWorkspaceName}-mlApi-dns-config'
        properties: {
            privateDnsZoneId: mlApiPrivateDnsZone.id
        }
      }
      {
        name: '${hubWorkspaceName}-mlNotebook-dns-config'
        properties: {
            privateDnsZoneId: mlNotebooksPrivateDnsZone.id
        }
      }
    ]
  }
  dependsOn: [
    mlApiPrivateDnsZoneVirtualNetworkLink
    mlNotebooksPrivateDnsZoneVirtualNetworkLink
  ]
}

// Private DNS Zone for AI Search
// - Enables custom DNS resolution for AI Search private endpoint
resource aiSearchPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.search.windows.net'  // Standard DNS zone for AI Search
  location: 'global'
}

// Link AI Search DNS Zone to VNet
resource aiSearchLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  parent: aiSearchPrivateDnsZone
  location: 'global'
  name: 'aiSearch-${suffix}-link'
  properties: {
    virtualNetwork: {
      id: vnet.id                        // Link to specified VNet
    }
    registrationEnabled: false           // Don't auto-register VNet resources
  }
}

// DNS Zone Group for AI Search
resource aiSearchDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: aiSearchPrivateEndpoint
  name: '${aiSearchName}-dns-group'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${aiSearchName}-dns-config'
        properties: {
          privateDnsZoneId: aiSearchPrivateDnsZone.id
        }
      }
    ]
  }
}

// Private DNS Zone for Storage
// - Enables custom DNS resolution for blob storage private endpoint
resource storagePrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.blob.${environment().suffixes.storage}'  // Dynamic DNS zone for storage
  location: 'global'
}

// Link Storage DNS Zone to VNet
resource storageLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  parent: storagePrivateDnsZone
  location: 'global'
  name: 'storage-${suffix}-link'
  properties: {
    virtualNetwork: {
      id: vnet.id                        // Link to specified VNet
    }
    registrationEnabled: false           // Don't auto-register VNet resources
  }
}

// DNS Zone Group for Storage
resource storageDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: storagePrivateEndpoint
  name: '${storageName}-dns-group'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${storageName}-dns-config'
        properties: {
          privateDnsZoneId: storagePrivateDnsZone.id
        }
      }
    ]
  }
}
