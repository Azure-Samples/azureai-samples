
# Introduction

This repository contains a collection of Jupyter notebooks demonstrating various use cases for interacting with the GPT-4 Turbo with Vision API, along with samples demonstrating how to use GPT-4 Turbo with Vision for Chat Completions via REST API. These examples provide practical guidance and accelerators for developers integrating GPT-4 Turbo with Vision functionalities in their applications.

## Contents
| Notebook | Description | Type |
|----------|-------------|-------|
| [Basic Image in GPT-4 Turbo with Vision](basic/basic_chatcompletions_example_restapi.ipynb) | Processing a single image input with GPT-4 Turbo with Vision. | Image |
| [Handling Multiple Images in GPT-4 Turbo with Vision](multiple_images/multiple_images_chatcompletions_example_restapi.ipynb) | Managing multiple image inputs in GPT-4 Turbo with Vision. | Image |
| [Enhancing GPT-4 Turbo with Vision with RAG and Custom Data](rag/rag_chatcompletions_example_restapi.ipynb) |  Enhancing capabilities by bringing custom data to augment image inputs in GPT-4 Turbo with Vision. | Image |
| [Enhancing GPT-4 Turbo with Vision with Grounding Techniques](enhancement_grounding/enhancement_grounding_chatcompletions_example_restapi.ipynb) | Applying grounding techniques to image inputs in GPT-4 Turbo with Vision. | Image |
| [Enhancing GPT-4 Turbo with Vision with OCR Technique](enhancement_OCR/enhancement_OCR_chatcompletions_example_restapi.ipynb) | Incorporating Optical Character Recognition (OCR) with image inputs in GPT-4 Turbo with Vision. | Image |
| [Enhancing GPT-4 Turbo with Vision with Face Attributes](face/face_chatcompletions_example_restapi.ipynb) | Utilize face attributes obtained from the face API to assess face image quality in GPT-4 Turbo with Vision. | Image |
| [Basic Video QnA in GPT-4 Turbo with Vision based on video index](video/video_chatcompletions_example_restapi.ipynb) | Conducting Q&A with video inputs (indexed) in GPT-4 Turbo with Vision. | Video |
| [Basic Video QnA in GPT-4 Turbo with Vision by manual sampling](video_by_manual_sampling/video_chatcompletions_example_restapi.ipynb) | Conducting Q&A with video inputs by manually sampling frames in GPT-4 Turbo with Vision. | Video |
| [Video Chunk Processing Sequentially in GPT-4 Turbo with Vision based on video index](video_chunk/video_chunk_chatcompletions_example_restapi.ipynb) | Sequential processing of video chunks (indexed) in GPT-4 Turbo with Vision. | Video |
| [Video Chunk Processing Sequentially in GPT-4 Turbo with Vision by manual sampling](video_chunk_by_manual_sampling/video_chunk_chatcompletions_example_restapi.ipynb) | Sequential processing of video chunks by manually sampling frames in GPT-4 Turbo with Vision. | Video |


## Installation
Install all Python modules and packages listed in the requirements.txt file using the below command.

```python
pip install -r requirements.txt
```

### Microsoft Azure Endpoints
In order to use REST API with Microsoft Azure endpoints, you need to set a series of configurations such as GPT-4V_DEPLOYMENT_NAME, OPENAI_API_BASE, OPENAI_API_VERSION.

```js
{
    "GPT-4V_DEPLOYMENT_NAME":"<GPT-4 Turbo with Vision Deployment Name>",
    "OPENAI_API_BASE":"https://<Your Azure Resource Name>.openai.azure.com",
    "OPENAI_API_VERSION":"<OpenAI API Version>",

    "VISION_API_ENDPOINT": "https://<Your Azure Vision Resource Name>.cognitiveservices.azure.com",

    "AZURE_SEARCH_SERVICE_ENDPOINT": "https://<Your Azure Search Resource Name>.search.windows.net",
    "AZURE_SEARCH_INDEX_NAME": "<Your Azure Search Index Name>",

    "FACE_API_ENDPOINT": "https://<Your Azure Face Resource Name>.cognitiveservices.azure.com"
}
``` 

### For getting started:
- Add "OPENAI_API_KEY", "VISION_API_KEY", "AZURE_SEARCH_QUERY_KEY" and "FACE_API_KEY" as variable name and \<Your API Key Value\>, \<Your VISION Key Value\>, \<Your SEARCH Query Key Value\>, and \<Your FACE Key Value\> as variable value in the environment variables.
<br>
One can get the OPENAI_API_KEY, VISION_API_KEY, AZURE_SEARCH_QUERY_KEY, and FACE_API_KEY values from the Azure Portal. Go to https://portal.azure.com, find your resource and then under "Resource Management" -> "Keys and Endpoints" look for one of the "Keys" values.
 <br>
      
      WINDOWS Users: 
         setx OPENAI_API_KEY ""
         setx VISION_API_KEY ""
         setx AZURE_SEARCH_QUERY_KEY ""
         setx FACE_API_KEY ""

      MACOS/LINUX Users: 
         export OPENAI_API_KEY=""
         export VISION_API_KEY=""
         export AZURE_SEARCH_QUERY_KEY=""
         export FACE_API_KEY=""

- To find your "OPENAI_API_BASE", "VISION_API_ENDPOINT", "AZURE_SEARCH_SERVICE_ENDPOINT", and "FACE_API_ENDPOINT",  go to https://portal.azure.com, find your resource and then under "Resource Management" -> "Keys and Endpoints" look for the "Endpoint" value.

Learn more about Azure OpenAI Service REST API [here](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference).


## Requirements
Python 3.8+ <br>
Jupyter Notebook 6.5.2


## Usage

Each notebook is self-contained and includes instructions specific to its scenario. Simply open a notebook in Jupyter and follow the steps outlined within it.

## Shared Functions

For convenience, commonly used functions across these notebooks are consolidated in [shared_functions.py](shared_functions.py). Import these functions in any notebook as needed.


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
