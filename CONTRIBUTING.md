# Contributing to Azure AI Samples

This repository is entirely open source and welcomes contributions! These are official examples for Azure AI used throughout documentation. Please read through the contributing guide below to avoid frustration!

## Contributor License Agreement
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

## Code of Conduct
This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

Help us keep this project open and inclusive. Please read and follow our [Code of Conduct](https://opensource.microsoft.com/codeofconduct/).


## Submitting a Pull Request (PR)

### Before Making Code Changes

1. Search the [repository](https://github.com/Azure-Samples/azureai-samples/pulls) for an open or closed PR
  that relates to your submission. You don't want to duplicate effort.
2. Determine whether this repository is the best place for the contribution.

   **Goals**: This repository contains notebooks and sample code that demonstrate how to develop and manage AI
   workflows using Azure AI. The samples in this repository should allow users to try out Azure AI scenarios from their
   local machine.

   **Non-goals**: This repository is not the place for long-form textual documentation. Documentation resources
   containing minimal or no code should be added in the [azure-docs repository](https://github.com/MicrosoftDocs/azure-docs).

### Making your Code Changes

#### Set up your development environment (one time setup)

##### 1. Make a fork

This repository follows a fork-based workflow. You should make your changes on your own fork, and make a PR to
contribute your changes.

1. [Make a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) of this repository.
2. Clone your fork
3. Add the original repository as a remote:

   ```shell
   git remote add upstream https://github.com/Azure-Samples/azureai-samples.git
   ```

##### 2. Install Dev Dependencies

From the root of your local repository, run:

```shell
python -m pip install -r dev_requirements.txt
```

##### 3. Set up pre-commit

[pre-commit](https://pre-commit.com/) is a tool that enables us to run code when committing to a local repository. We
use this to automate running code formatters, linters, etc...

To install pre-commit in the repository, run the following from the root of the repository:

```shell
pre-commit install
```

`pre-commit` will run automatically when you commit changes, but you can also manually run it using 
`pre-commit run --all-files`.

#### Write your contribution

If you are writing/updating a sample, please follow this guidance on how the samples should be structured:

* Please create a **separate** directory for each authored sample. Each directory should contain:
    * A descriptive README in the root folder of your sample following the [README template].
    * Your sample
      * If you're adding a Python sample, please follow the [Jupyter Notebook template].
    * Any other supporting files for your sample (datasets, scripts, etc...). Samples should ideally only depend on
      files within their directory.

#### Submit your pull request

* Commit your changes using a descriptive commit message
* [Push your changes to your fork](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository).
* [Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
* **Review the checklist in the PR**.
* If we suggest changes then:
  * Make the required updates.
  * Rebase your fork and force push to your GitHub repository (this will update your Pull Request):

    ```shell
    git rebase master -i
    git push -f
    ```

That's it! Thank you for your contribution!

[readme template]: ./notebooks/README-template.md
[jupyter notebook template]: ./notebooks/template.ipynb
