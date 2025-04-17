# RBAC roles

Make sure both developers and end users have the following permissions: 

* `Microsoft.MachineLearningServices/workspaces/agents/read `
* `Microsoft.MachineLearningServices/workspaces/agents/action `
* `Microsoft.MachineLearningServices/workspaces/agents/delete `

If you want to create custom permissions, make sure they have: 

* `agents/*/read` 
* `agents/*/action` 
* `agents/*/delete` 