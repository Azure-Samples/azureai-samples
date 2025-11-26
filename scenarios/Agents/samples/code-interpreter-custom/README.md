# Custom Code Interpreter with Session Pool MCP server

This provides example Bicep code for setting up a Container Apps dynamic session pool
with a custom code interpreter image, as well as Python client code demonstrating
how to use it with a Foundry Hosted Agent.

- The `az` CLI
- The `uv` or `pip` Python package managers

## Running code sample

### Enable MCP server for dynamic sessions

This is required to enable the preview feature.

```console
az feature register --namespace Microsoft.App --name SessionPoolsSupportMCP
az provider register -n Microsoft.App
```

### Create a dynamic session pool with a code interpreter image

Run the following, substituting the appropriate values. Set parameters if you wish.

```console
az deployment group create \
    --name custom-code-interpreter \
    --subscription <your_subscription> \
    --resource-group <your_resource_group> \
    --template-file ./infra.bicep
```

This can take a while!

### Use the custom code interpreter in an agent

Copy the [`.env.sample`](./.env.sample) file to `.env` and fill in the values with
the output of the above deployment, which you can find in the Web Portal under the
resource group.

Install the Python dependencies (`uv sync` or `pip install`). Finally, run `./main.py`.

## Limitations

File input/output and use of file stores are not directly supported in APIs, so you must use URLs (such as data URLs for small files and Azure Blob Service SAS URLs for large ones) to get data in and out.

## References

- [Azure Container Apps Dynamic Sessions](/azure/container-apps/sessions)
- [Session Pools with Custom Containers](/azure/container-apps/session-pool#custom-container-pool)
