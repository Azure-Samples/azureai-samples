//params
param locations array
param rgLocationsDefinition string
param locationMatchDefinition string

//vars
var rgLocations = 'Allowed locations for resource groups'
var locationMatch = 'Audit resource location matches resource group location'

//deploy policy assignments

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

output rgLocation string = allowRgLocations.name
output locationMatch string = resourceLocationMatch.name
