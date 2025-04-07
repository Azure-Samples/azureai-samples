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
python -m pip install -r dev-requirements.txt
```

##### 3. Set up pre-commit

[pre-commit](https://pre-commit.com/) is a tool that enables us to run code when committing to a local repository. We
use this to automate running code formatters, linters, etc...

To enable `pre-commit`, run the following from the root of the repository:

```shell
pre-commit install
```

`pre-commit` will now automatically run a series of code quality checks when you commit changes, which
will accelerate the identification of issues that will be flagged when the PR is submitted.

If needed, you can manually run `pre-commit` against all files  with `pre-commit run --all-files`. See
[the documentation for `pre-commit run`](https://pre-commit.com/#pre-commit-run) for more information.

Note: 

pre-commit will check for any exposed secrets in your code. If you'd like to leave a placeholder for a secret, use this syntax to avoid being flagged by pre-commit:

```python
import os

os.environ["AZURE_SUBSCRIPTION_ID"] = ""
os.environ["AZURE_RESOURCE_GROUP"] = ""
os.environ["AZURE_PROJECT_NAME"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = ""
...
```


#### Write your contribution

If you are writing/updating a sample, please follow this guidance on how the samples should be structured.

Note that samples are organized by scenario, find the one best-suited for your sample or propose a new one for consideration.

* Please create a **separate** directory for each authored sample, making sure to create it under the appropriate top-level scenario directory. Each sample's directory should contain:
    * A descriptive README in the root folder of your sample following the [README template].
    * Your sample
      * If you're adding a Python sample, please follow the [Jupyter Notebook template].
    * Any other supporting files for your sample (datasets, scripts, etc...). Samples should ideally only depend on files within their directory.

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

> [!IMPORTANT]
>
> You should expect to budget time to engage with reviewers (responding to comments, fixing PR checks) before your PR is merged in. This is especially
> relevant if your contribution is _time-sensitive_.
>
> Adhering to the guidance in this document (i.e [using pre-commit](#3-set-up-pre-commit), [using provided templates](#write-your-contribution)) ***will***
> help expedite the review process.

#### Resolve Failing Pull Request Checks


> [!IMPORTANT]
>
> This repository requires approval from someone with write access for pull request checks
> to run against a PR, to avoid abuse of live resources.
>
> All of the PR checks can also be run from developers machine, which should prevent the approval
> processes from unnecessarily lengthening the feedback cycle.

> [!NOTE]
> If you are a Microsoft employee, you can skip the approval process for PR checks by:
>
>   * Joining the "[Azure-Samples](https://github.com/Azure-Samples)" organization
>   * [Setting your org membership visibility to public](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-membership-in-organizations/publicizing-or-hiding-organization-membership#changing-the-visibility-of-your-organization-membership)
>

##### pre-commit

###### black

[black](https://github.com/psf/black) is a code formatter for Python and Jupyter notebooks.

**How to Fix**: If the `pre-commit` check is failing on your PR because of `black`, just run `pre-commit run black --all-files` and commit the changes.

###### nb-clean

[nb-clean](https://github.com/srstevenson/nb-clean) that removes metadata from Jupyter Notebooks to make them more ammenable to version control.

**How to Fix**: If the `nb-clean` check is failing on your PR because of `nb-clean`, just run `pre-commit run nb-clean --all-files` and commit the changes.

###### ruff

[ruff](https://github.com/astral-sh/ruff) is a linter for Python and Jupyter Notebooks.

**How to Fix**: If the `pre-commit` step is failing on your PR because of `ruff`:
  * ruff makes an attempt to automatically fix issues it detects. You can run `pre-commit run ruff --all-files` and commit any changes.
  * Issues that ruff can't fix should be manually updated and committed. See ruff's [rule list](https://docs.astral.sh/ruff/rules/) for more info on issues it reports.

### Discoverability

Examples in this repository can be indexed in the [Microsoft code samples browser](https://docs.microsoft.com/samples), enabling organic discoverability. To accomplish this, add the required YAML frontmatter at the top of the `README.md`

The YAML frontmatter format looks like this:

```YAML
---
page_type: sample
languages:
- language1
- language2
products:
- ai-services
description: Example description.
---
```

Edit the product, description, and languages as needed.

* You can find all valid product options [here](https://review.learn.microsoft.com/en-us/help/platform/metadata-taxonomies?branch=main#product).
* You can find valid language options [here](https://review.learn.microsoft.com/en-us/help/platform/metadata-taxonomies?branch=main#dev-lang).

The Code Samples browser content is updated twice a week, so it may take a few days for your changes to be reflected.

[readme template]: ./.infra/templates/README-template.md
[jupyter notebook template]: ./.infra/templates/template.ipynb

