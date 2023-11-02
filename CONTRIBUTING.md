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

## Found an Issue?
If you find a bug in the source code or a mistake in the documentation, you can help us by
[submitting an issue](#submit-issue) to the GitHub Repository. Even better, you can
[submit a Pull Request](#submit-pr) with a fix.

## Want a Feature?
You can *request* a new feature by [submitting an issue](#submit-issue) to the GitHub
Repository. If you would like to *implement* a new feature, please submit an issue with
a proposal for your work first, to be sure that we can use it.

* **Small Features** can be crafted and directly [submitted as a Pull Request](#submit-pr).

## Submission Guidelines

### Submitting an Issue
Before you submit an issue, search the archive, maybe your question was already answered.

If your issue appears to be a bug, and hasn't been reported, open a new issue.
Help us to maximize the effort we can spend fixing issues and adding new
features, by not reporting duplicate issues.  Providing the following information will increase the
chances of your issue being dealt with quickly:

* **Overview of the Issue** - if an error is being thrown a non-minified stack trace helps
* **Version** - what version is affected (e.g. 0.1.2)
* **Motivation for or Use Case** - explain what are you trying to do and why the current behavior is a bug for you
* **Browsers and Operating System** - is this a problem with all browsers?
* **Reproduce the Error** - provide a live example or a unambiguous set of steps
* **Related Issues** - has a similar issue been reported before?
* **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point to what might be
  causing the problem (line of code or commit)

You can file new issues by providing the above information at the corresponding repository's issues link: https://github.com/[organization-name]/[repository-name]/issues/new].

### Submitting a Pull Request (PR)

#### Before Making Code Changes

1. Search the [repository](https://github.com/Azure-Samples/azureai-samples/pulls) for an open or closed PR
  that relates to your submission. You don't want to duplicate effort.
2. Determine whether this repository is the best place for the contribution.

   **Goals**: This repository contains notebooks and sample code that demonstrate how to develop and manage AI
   workflows using Azure AI. The samples in this repository should allow users to try out Azure AI scenarios from their
   local machine.

   **Non-goals**: This repository is not the place for long-form textual documentation. Documentation resources
   containing minimal or no code should be added in the [azure-docs repository](https://github.com/MicrosoftDocs/azure-docs).

* Make your changes in a new git fork
  
   - Create a fork of this repository. This will create a copy of this repository in your account.
   - Go to a git terminal, clone your forked repository, navigate to the root folder, and run 
  `git remote add upstream https://github.com/Azure-Samples/azureai-samples.git` to connect your fork with the original repository.
   - Verify the new upstream repository you've specified for your fork with ` git remote -v`.

* Add a descriptive [README] in the root folder of your sample following the [README template](https://github.com/Azure-Samples/azureai-samples/blob/main/notebooks/README-template.ipynb). If you're adding a Python sample, please ensure it follows the [Jupyter notebook template](https://github.com/Azure-Samples/azureai-samples/blob/main/notebooks/template.ipynb).
* Commit your changes using a descriptive commit message
* Push your fork to GitHub
* In GitHub, create a pull request and review the PR checklist.
* If we suggest changes then:
  * Make the required updates.
  * Rebase your fork and force push to your GitHub repository (this will update your Pull Request):

    ```shell
    git rebase master -i
    git push -f
    ```

That's it! Thank you for your contribution!
