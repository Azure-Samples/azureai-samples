param subnetName string
param virtualNetworkName string
param virtualMachineName string

// New parameters
param location string = resourceGroup().location
param adminUsername string
param adminPublicKey string
param vmSize string = 'Standard_D2s_v3'
param bastionName string = '${virtualNetworkName}-bastion'


resource existingVirtualNetwork 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name: virtualNetworkName
  scope: resourceGroup()
}

// Get existing subnet in the virtual network
resource cxSubnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' existing = {
  parent: existingVirtualNetwork
  name: subnetName
}

// Create AzureBastionSubnet in the existing virtual network
resource bastionSubnet 'Microsoft.Network/virtualNetworks/subnets@2023-05-01' = {
  parent: existingVirtualNetwork
  name: 'AzureBastionSubnet' // This specific name is required by Azure Bastion
  properties: {
    addressPrefix: '172.16.1.0/26' // Using the same prefix as your reference
    privateEndpointNetworkPolicies: 'Disabled'
    privateLinkServiceNetworkPolicies: 'Enabled'
  }
}

// Create new public IP for Bastion following Azure best practices
resource bastionPublicIP 'Microsoft.Network/publicIPAddresses@2023-05-01' = {
  name: '${bastionName}-pip'
  location: location
  sku: {
    name: 'Standard' // Required for Azure Bastion
    tier: 'Regional'
  }
  properties: {
    publicIPAllocationMethod: 'Static' // Required for Azure Bastion
    publicIPAddressVersion: 'IPv4'
    idleTimeoutInMinutes: 4
    dnsSettings: {
      domainNameLabel: toLower('${bastionName}-${uniqueString(resourceGroup().id)}')
    }
  }
  zones: ['1', '2', '3'] // Zone redundant for high availability
}

// Create Azure Bastion with Standard SKU for enhanced features
resource bastion 'Microsoft.Network/bastionHosts@2023-05-01' = {
  name: bastionName
  location: location
  sku: {
    name: 'Standard' // Standard SKU supports file copy, native client, and tunneling
  }
  properties: {
    enableFileCopy: true
    enableTunneling: true
    enableIpConnect: true
    scaleUnits: 2 // For better performance
    ipConfigurations: [
      {
        name: 'IpConf'
        properties: {
          publicIPAddress: {
            id: bastionPublicIP.id
          }
          subnet: {
            id: bastionSubnet.id
          }
        }
      }
    ]
  }
}

// Create VM NSG with Azure best practice security rules
resource vmNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: '${virtualMachineName}-nsg'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowSSHFromBastion'
        properties: {
          priority: 100
          protocol: 'Tcp'
          access: 'Allow'
          direction: 'Inbound'
          sourceAddressPrefix: 'VirtualNetwork'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '22'
          description: 'Allow SSH access from Bastion only'
        }
      }
      {
        name: 'DenyAllInbound'
        properties: {
          priority: 4096
          protocol: '*'
          access: 'Deny'
          direction: 'Inbound'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
          description: 'Deny all other inbound traffic'
        }
      }
    ]
  }
  tags: {
    vm: virtualMachineName
  }
}

// Create public IP for VM with Standard SKU
resource vmPublicIP 'Microsoft.Network/publicIPAddresses@2023-05-01' = {
  name: '${virtualMachineName}-pip'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Regional'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
    publicIPAddressVersion: 'IPv4'
    dnsSettings: {
      domainNameLabel: toLower('${virtualMachineName}-${uniqueString(resourceGroup().id)}')
    }
  }
  tags: {
    vm: virtualMachineName
  }
}

// Create network interface for VM with NSG
resource vmNic 'Microsoft.Network/networkInterfaces@2023-05-01' = {
  name: '${virtualMachineName}-nic'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          subnet: {
            id: cxSubnet.id
          }
          privateIPAllocationMethod: 'Dynamic'
          publicIPAddress: {
            id: vmPublicIP.id
          }
        }
      }
    ]
    networkSecurityGroup: {
      id: vmNsg.id
    }
    enableAcceleratedNetworking: true // For better network performance
  }
  tags: {
    vm: virtualMachineName
  }
}

// Create Ubuntu 24.04 virtual machine with secure configurations
resource virtualMachine 'Microsoft.Compute/virtualMachines@2023-09-01' = {
  name: virtualMachineName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: vmSize
    }
    storageProfile: {
      imageReference: {
        publisher: 'canonical'
        offer: 'ubuntu-24_04-lts'
        sku: 'server'
        version: 'latest'
      }
      osDisk: {
        name: '${virtualMachineName}-osdisk'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Premium_LRS'
        }
        caching: 'ReadWrite'
        deleteOption: 'Delete' // Clean up disk when VM is deleted
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: vmNic.id
          properties: {
            deleteOption: 'Delete' // Clean up NIC when VM is deleted
          }
        }
      ]
    }
    osProfile: {
      computerName: virtualMachineName
      adminUsername: adminUsername
      linuxConfiguration: {
        disablePasswordAuthentication: true
        ssh: {
          publicKeys: [
            {
              path: '/home/${adminUsername}/.ssh/authorized_keys'
              keyData: adminPublicKey
            }
          ]
        }
        patchSettings: {
          patchMode: 'AutomaticByPlatform' // Enable automatic OS updates
          assessmentMode: 'ImageDefault'
        }
      }
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true // Enable boot diagnostics for troubleshooting
      }
    }
  }
  tags: {
    application: 'agents'
    environment: 'development'
  }
}

// Add Azure Monitor agent for better monitoring and insights
resource monitoringAgent 'Microsoft.Compute/virtualMachines/extensions@2023-09-01' = {
  parent: virtualMachine
  name: 'AzureMonitorLinuxAgent'
  location: location
  properties: {
    publisher: 'Microsoft.Azure.Monitor'
    type: 'AzureMonitorLinuxAgent'
    typeHandlerVersion: '1.0'
    autoUpgradeMinorVersion: true
    enableAutomaticUpgrade: true
  }
}

// Outputs
output vmId string = virtualMachine.id
output vmName string = virtualMachine.name
output vmFqdn string = vmPublicIP.properties.dnsSettings.fqdn
output bastionId string = bastion.id
output bastionFqdn string = bastionPublicIP.properties.dnsSettings.fqdn
