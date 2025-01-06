import openai
import os


class AzureOpenAITarget(object):
    def __init__(self):
        self._api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
        self._azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self._azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        self._api_key = os.environ.get("AZURE_OPENAI_API_KEY")

    def __call__(self, *, messages, **kwargs):
        client = openai.AzureOpenAI(
            # azure_ad_token_provider=self.token_provider,
            api_key=self._api_key,
            api_version=self._api_version,
            azure_endpoint=self._azure_endpoint,
            azure_deployment=self._azure_deployment,
        )
        response = client.chat.completions.create(
            model=self._azure_deployment,
            messages=messages,
        )
        response = response.choices[0].message.content
        return {"response": response}
