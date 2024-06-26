# %% [markdown]
# <h1 align ="center"> Shared Functions</h1>
# <hr>

# %%
import json
import os
import requests
import time
import cv2
from moviepy.editor import VideoFileClip
import base64
from pathlib import Path

current_script_dir = Path(__file__).parent

# %% [markdown]
# ### Setup Parameters
#
#
# Here we will load the configurations from _config.json_ file to
# setup deployment_name, openai_api_base, openai_api_key and openai_api_version.

# %%
# Load config values
with Path(current_script_dir / "config.json").open() as config_file:
    config_details = json.load(config_file)

# Setting up the deployment name
deployment_name = config_details["GPT-4V_DEPLOYMENT_NAME"]

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai_api_base = config_details["OPENAI_API_BASE"]

# The API key for your Azure OpenAI resource.
openai_api_key = os.getenv("OPENAI_API_KEY")

# Currently OPENAI API have the following versions available: 2022-12-01.
# All versions follow the YYYY-MM-DD date structure.
openai_api_version = config_details["OPENAI_API_VERSION"]


# %% [markdown]
# ## Funciontion to Call GPT-4 Turbo with Vision
def call_GPT4V(messages: list) -> object:
    # Construct the API request URL
    api_url = (
        f"{openai_api_base}/openai/deployments/{deployment_name}" f"/chat/completions?api-version={openai_api_version}"
    )

    # Including the api-key in HTTP headers
    headers = {
        "Content-Type": "application/json",
        "api-key": openai_api_key,
        "x-ms-useragent": "Azure-GPT-4V-video/1.0.0",
    }

    # Payload for the request
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800,
    }

    # Send the request and handle the response
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")


# %% [markdown]
# ## Funciontion to Call GPT-4 Turbo with Vision API with Image


# %%
# Define GPT-4 Turbo with Vision API call with image
def call_GPT4V_image(
    messages: object,
    ocr: bool = False,
    grounding: bool = False,
    face: bool = False,
    in_context: object = None,
    vision_api: object = None,
) -> object:
    # Construct the API request URL
    if ocr or grounding or in_context is not None:
        api_url = (
            f"{openai_api_base}/openai/deployments/{deployment_name}"
            f"/extensions/chat/completions?api-version={openai_api_version}"
        )
    else:
        api_url = (
            f"{openai_api_base}/openai/deployments/{deployment_name}/chat/completions?api-version={openai_api_version}"
        )

    # Including the api-key in HTTP headers
    headers = {
        "Content-Type": "application/json",
        "api-key": openai_api_key,
        "x-ms-useragent": "Azure-GPT-4V-image/1.0.0",
    }

    if face:
        headers["x-ms-useragent"] = "Azure-GPT-4V-image-face/1.0.0"

    # Payload for the request
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800,
    }

    if ocr or grounding:
        payload["enhancements"] = {
            "ocr": {"enabled": ocr},  # Enable OCR enhancement
            "grounding": {"enabled": grounding},  # Enable grounding enhancement
        }

    data_sources = []

    if in_context is not None:
        data_sources.append(
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": in_context.get("endpoint"),
                    "key": in_context.get("key"),
                    "indexName": in_context.get("indexName"),
                },
            }
        )

    if vision_api is not None:
        data_sources.append(
            {
                "type": "AzureComputerVision",
                "parameters": {
                    "endpoint": vision_api.get("endpoint"),
                    "key": vision_api.get("key"),
                },
            }
        )

    if data_sources:
        payload["dataSources"] = data_sources

    # Send the request and handle the response
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")


# %% [markdown]
# ## Funciontion to Call GPT-4 Turbo with Vision API with Video Index


# %%
# Define GPT-4 Turbo with Vision API call with video index
def call_GPT4V_video(messages: str, vision_api: object, video_index: object) -> object:
    # Construct the API request URL
    api_url = (
        f"{openai_api_base}/openai/deployments/{deployment_name}"
        f"/extensions/chat/completions?api-version={openai_api_version}"
    )

    # Including the api-key in HTTP headers
    headers = {
        "Content-Type": "application/json",
        "api-key": openai_api_key,
        "x-ms-useragent": "Azure-GPT-4V-video/1.0.0",
    }

    # Payload for the request
    payload = {
        "model": "gpt-4-vision-preview",
        "dataSources": [
            {
                "type": "AzureComputerVisionVideoIndex",
                "parameters": {
                    "computerVisionBaseUrl": f"{vision_api.get('endpoint')}/computervision",
                    "computerVisionApiKey": vision_api.get("key"),
                    "indexName": video_index.get("video_index_name"),
                    "videoUrls": [video_index.get("video_SAS_url")],
                },
            }
        ],
        "enhancements": {"video": {"enabled": True}},
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800,
    }

    # Send the request and handle the response
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")


# %% [markdown]
# ## Function to Create Video Index


# %%
def create_video_index(vision_api_endpoint: str, vision_api_key: str, index_name: str) -> object:
    url = f"{vision_api_endpoint}/computervision/retrieval/indexes/{index_name}?api-version=2023-05-01-preview"
    headers = {"Ocp-Apim-Subscription-Key": vision_api_key, "Content-Type": "application/json"}
    data = {"features": [{"name": "vision", "domain": "surveillance"}, {"name": "speech"}]}
    return requests.put(url, headers=headers, data=json.dumps(data))


def add_video_to_index(
    vision_api_endpoint: str, vision_api_key: str, index_name: str, video_url: str, video_id: str
) -> object:
    url = (
        f"{vision_api_endpoint}/computervision/retrieval/indexes/{index_name}"
        f"/ingestions/my-ingestion?api-version=2023-05-01-preview"
    )
    headers = {"Ocp-Apim-Subscription-Key": vision_api_key, "Content-Type": "application/json"}
    data = {
        "videos": [{"mode": "add", "documentId": video_id, "documentUrl": video_url}],
        "generateInsightIntervals": False,
        "moderation": False,
        "filterDefectedFrames": False,
        "includeSpeechTranscrpt": True,
    }
    return requests.put(url, headers=headers, data=json.dumps(data))


def wait_for_ingestion_completion(
    vision_api_endpoint: str, vision_api_key: str, index_name: str, max_retries: int = 30
) -> bool:
    url = (
        f"{vision_api_endpoint}/computervision/retrieval/indexes/{index_name}/ingestions?api-version=2023-05-01-preview"
    )
    headers = {"Ocp-Apim-Subscription-Key": vision_api_key}
    retries = 0
    while retries < max_retries:
        time.sleep(10)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            state_data = response.json()
            if state_data["value"][0]["state"] == "Completed":
                print(state_data)
                print("Ingestion completed.")
                return True
            if state_data["value"][0]["state"] == "Failed":
                print(state_data)
                print("Ingestion failed.")
                return False
        retries += 1
    return False


def process_video_indexing(
    vision_api_endpoint: str, vision_api_key: str, video_index_name: str, video_SAS_url: str, video_id: str
) -> None:
    # Step 1: Create an Index
    response = create_video_index(vision_api_endpoint, vision_api_key, video_index_name)
    print(response.status_code, response.text)

    # Step 2: Add a video file to the index
    response = add_video_to_index(vision_api_endpoint, vision_api_key, video_index_name, video_SAS_url, video_id)
    print(response.status_code, response.text)

    # Step 3: Wait for ingestion to complete
    if not wait_for_ingestion_completion(vision_api_endpoint, vision_api_key, video_index_name):
        print("Ingestion did not complete within the expected time.")


def call_face_API(image_file_path: str, face_api_endpoint: str, face_api_key: str) -> object:
    """
    Calls a face recognition API and returns attributes of faces detected in the image.

    Args:
    image_file_path (str): Path to the image file.
    face_api_endpoint (str): Endpoint URL of the face API.
    face_api_key (str): Subscription key for the face API.

    Returns:
    tuple: A tuple containing two objects with face attributes from different API parameters.
    """

    def make_api_request(image: bytes, params: dict) -> dict:
        """Helper function to make API request and return response."""
        try:
            face_api_url = face_api_endpoint + "/face/v1.0/detect"
            response = requests.post(face_api_url, params=params, headers=headers, data=image)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to make the request. Error: {e}")
            return None

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": face_api_key,
        "x-ms-useragent": "Azure-GPT-4V-image-face/1.0.0",
    }

    params_01 = {
        "returnFaceId": "false",
        "returnFaceLandmarks": "false",
        "returnFaceAttributes": ",".join(
            [
                "glasses",
                "occlusion",
                "accessories",
                "blur",
                "exposure",
                "noise",
            ]
        ),
    }
    params_03 = {
        "returnFaceId": "false",
        "returnFaceLandmarks": "false",
        "detectionModel": "detection_03",
        "recognitionModel": "recognition_04",
        "returnFaceAttributes": ",".join(["mask", "headPose", "qualityForRecognition"]),
    }

    try:
        with Path(image_file_path).open("rb") as image_file:
            image = image_file.read()

        attributes_01 = make_api_request(image, params_01)
        attributes_03 = make_api_request(image, params_03)

        return attributes_01, attributes_03

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def download_video(sas_url: str, local_file_path: str) -> bool:
    try:
        response = requests.get(sas_url, stream=True)
        if response.status_code == 200:
            with Path(local_file_path).open("wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return True

        print(f"Download failed with status code: {response.status_code}")
        return False
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return False


def sample_frames(clip: VideoFileClip, num_frames: int) -> list:
    frame_times = [int(i * clip.duration / num_frames) for i in range(num_frames)]
    frames = [(t, clip.get_frame(t)) for t in frame_times]
    return [
        (frame[0], base64.b64encode(cv2.imencode(".jpg", frame[1])[1].tostring()).decode("utf-8")) for frame in frames
    ]
