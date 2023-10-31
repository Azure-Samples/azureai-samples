## Compute targets for inference

When performing inference, Azure Machine Learning creates a Docker container that hosts the model and associated resources needed to use it. This container is then used in a compute target.

## Azure Machine Learning compute (managed)

A managed compute resource is created and managed by Azure Machine Learning. This compute is optimized for machine learning workloads. Azure Machine Learning compute clusters and [compute instances](concept-compute-instance.md) are the only managed computes.

You can create Azure Machine Learning compute instances or compute clusters from:

* Azure Machine Learning studio.
* The Python SDK and the Azure CLI:
    * Compute instance.
    * Compute cluster.
* An Azure Resource Manager template. For an example template, see [Create an Azure Machine Learning compute cluster](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-compute-create-amlcompute).

When created, these compute resources are automatically part of your workspace, unlike other kinds of compute targets.

|Capability  |Compute cluster  |Compute instance  |
|---------|---------|---------|
|Single- or multi-node cluster     |    **&check;**       |    Single node cluster     |
|Autoscales each time you submit a job     |     **&check;**      |         |
|Automatic cluster management and job scheduling     |   **&check;**        |     **&check;**      |
|Support for both CPU and GPU resources     |  **&check;**         |    **&check;**       |

> [!NOTE]
> To avoid charges when the compute is idle:
> * For compute *cluster* make sure the minimum number of nodes is set to 0.
> * For a compute *instance*, enable idle shutdown.
