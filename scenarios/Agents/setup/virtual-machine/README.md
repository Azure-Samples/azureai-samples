# Virtual Machine Setup for Azure AI Agents

This directory contains tools and scripts to configure virtual machines for running Azure AI Agents scenarios.

## Overview

The resources in this directory help you set up and configure virtual machines optimized for Azure AI agent development, testing, and deployment. These scripts automate the provisioning and configuration process to ensure a consistent environment for AI agent operations.

## Prerequisites

- Azure subscription with contributor access
- Azure CLI installed and configured
- Bash shell environment (Linux, macOS, or WSL on Windows)
- Sufficient quota for the VM sizes you intend to deploy

## Getting Started

### Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/Azure/azureai-samples.git
    cd azureai-samples/scenarios/Agents/setup/virtual-machine
    ```

2. Run the setup script:
    ```bash
    ./setup.sh
    ```

### Configuration Options

The setup can be customized by modifying the following parameters in the script or providing them as environment variables:

- `VM_SIZE`: Size of the virtual machine (default: Standard_D4s_v3)
- `LOCATION`: Azure region for deployment (default: eastus)
- `VM_NAME`: Name of the virtual machine (default: ai-agent-vm)
- `RESOURCE_GROUP`: Resource group name (default: ai-agent-resources)

## Deploy

## Deploy
[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fvirtual-machine%2Fazuredeploy.json)
## Features

- Automated VM provisioning with optimal settings for AI workloads
- Pre-installed AI development tools and dependencies
- Network security configuration for agent communication
- Integration with Azure AI services

## Step to connect to VS Code

You can connect to your Azure VM directly from Visual Studio Code using the Remote SSH extension. Here's how to set it up on Windows and Linux:

Windows
Install Required Extensions

Open VS Code and install the "Remote - SSH" extension
Install "Azure Account" and "Azure Resources" extensions
Configure SSH

Open File Explorer and navigate to C:\Users\YourUsername\.ssh
Place your existing private key in this folder (the one that pairs with the public key deployed to the VM)
Create or edit the file config in this folder with:
Connect through Azure Portal

Example SSH Config
```
Host ubuntu24-vm
  User azureuser
  HostName <YOUR_VM_IP_OR_DNS_NAME>
  IdentityFile /C:/Users/<username>/.ssh/project-vm.pem
```

Open VS Code command palette (Ctrl+Shift+P)
Type "Azure: Sign In" and complete the authentication
Select the Azure icon in the Activity Bar
Expand your subscription and locate your VM
Right-click and choose "Connect to Host in Current Window"
Connect Directly via Remote SSH

Click the green >< icon in the bottom-left corner of VS Code
Select "Connect to Host..."
Choose your VM from the list
VS Code will open a new window connected to your VM

## Troubleshooting

- **Deployment Failures**: Check Azure activity logs and ensure you have sufficient quota
- **Connection Issues**: Verify network security group settings and that you have the correct SSH keys
- **Performance Problems**: Consider upgrading to a VM with more resources

## Additional Resources

- [Azure AI Agents Documentation](https://learn.microsoft.com/azure/ai-services/agents/)
- [Azure Virtual Machines Documentation](https://learn.microsoft.com/azure/virtual-machines/)
- [Azure AI Services](https://learn.microsoft.com/azure/ai-services/)

## Contributing

Please see the [CONTRIBUTING.md](../../../../CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](../../../../LICENSE) file for details.
