//params
param locations array
param allowedLocationsDefintion string
param rgLocationsDefinition string
param locationMatchDefinition string

//vars
var allowedLocations = 'Allowed locations'
var rgLocations = 'Allowed locations for resource groups'
var locationMatch = 'Audit resource location matches resource group location'

//deploy policy assignments

resource allowLocations 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'allowed-locations'
  properties: {
    displayName: allowedLocations
    policyDefinitionId: allowedLocationsDefintion
    parameters: {
      listOfAllowedLocations: {
        value: locations
      }
    }
  }
}

resource allowRgLocations 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'rg-locations'
  properties: {
    displayName: rgLocations
    policyDefinitionId: rgLocationsDefinition
    parameters: {
      listOfAllowedLocations: {
        value: locations
      }
    }
  }
}

resource resourceLocationMatch 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'location-match'
  properties: {
    displayName: locationMatch
    policyDefinitionId: locationMatchDefinition
  }
}

