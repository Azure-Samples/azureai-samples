import os
from dotenv import load_dotenv
import openai

load_dotenv(override=True)

open_ai_endpoint = os.getenv("OPEN_AI_ENDPOINT")
open_ai_key = os.getenv("OPEN_AI_KEY")
open_ai_deployment_name = os.getenv("OPEN_AI_DEPLOYMENT_NAME")

api_version = "2024-02-15-preview"

client = openai.AzureOpenAI(api_key=open_ai_key, azure_endpoint=open_ai_endpoint, api_version=api_version)
