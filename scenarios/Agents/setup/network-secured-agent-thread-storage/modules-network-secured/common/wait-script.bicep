param name string
param location string
param retentionTime string = 'PT1H'  // Retention duration

resource waitScript 'Microsoft.Resources/deploymentScripts@2023-08-01' = {
  name: name
  location: location
  kind: 'AzurePowerShell'
  properties: {
    azPowerShellVersion: '10.0'
    scriptContent: '''
      Write-Output "Starting wait script..."
      Start-Sleep -Seconds 120
      Write-Output "Wait completed. Proceeding with deployment..."
    '''
    retentionInterval: retentionTime
    cleanupPreference: 'Always'
  }
}

output scriptName string = waitScript.name
