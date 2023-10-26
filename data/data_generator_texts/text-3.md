### Supported VM series and sizes

> [!NOTE]
> H-series virtual machine series will be retired on August 31, 2022. Create compute instance and compute clusters with alternate VM sizes. Existing compute instances and clusters with H-series virtual machines will not work after August 31, 2022.

When you select a node size for a managed compute resource in Azure Machine Learning, you can choose from among select VM sizes available in Azure. Azure offers a range of sizes for Linux and Windows for different workloads. To learn more, see VM types and sizes.

There are a few exceptions and limitations to choosing a VM size:

* Some VM series aren't supported in Azure Machine Learning.
* There are some VM series, such as GPUs and other special SKUs, which may not initially appear in your list of available VMs.  But you can still use them, once you request a quota change. For more information about requesting quotas, see Request quota increases.

> [!NOTE]
> Azure Machine Learning doesn't support all VM sizes that Azure Compute supports. To list the available VM sizes, use one of the following methods:
> * [REST API](https://github.com/Azure/azure-rest-api-specs/blob/master/specification/machinelearningservices/resource-manager/Microsoft.MachineLearningServices/stable/2020-08-01/examples/ListVMSizesResult.json)
> * The Azure CLI extension 2.0 for machine learning command, az ml compute list-sizes.

If using the GPU-enabled compute targets, it is important to ensure that the correct CUDA drivers are installed in the training environment. Use the following table to determine the correct CUDA version to use:

| **GPU Architecture**  | **Azure VM Series** | **Supported CUDA versions** |
|------------|------------|------------|
| Ampere | NDA100_v4 | 11.0+ |
| Turing | NCT4_v3 | 10.0+ |
| Volta | NCv3, NDv2 | 9.0+ |
| Pascal | NCv2, ND | 9.0+ |
| Maxwell | NV, NVv3 | 9.0+ |
| Kepler | NC, NC Promo| 9.0+ |

In addition to ensuring the CUDA version and hardware are compatible, also ensure that the CUDA version is compatible with the version of the machine learning framework you are using: 

- For PyTorch, you can check the compatibility by visiting [Pytorch's previous versions page](https://pytorch.org/get-started/previous-versions/).
- For Tensorflow, you can check the compatibility by visiting [Tensorflow's build from source page](https://www.tensorflow.org/install/source#gpu).
