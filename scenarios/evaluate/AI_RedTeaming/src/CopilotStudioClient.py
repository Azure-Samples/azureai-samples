"""
Based on the example at https://github.com/microsoft/Agents-for-python
Will be updated with the latest changes from the Copilot Studio client implementation.
"""

from os import environ
from pathlib import Path
from typing import Optional
import logging

from msal import PublicClientApplication
from msal_extensions import build_encrypted_persistence, FilePersistence, PersistedTokenCache

from microsoft.agents.copilotstudio.client import ConnectionSettings, CopilotClient, PowerPlatformCloud, AgentType


class McsConnectionSettings(ConnectionSettings):
    def __init__(
        self,
        app_client_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        environment_id: Optional[str] = None,
        agent_identifier: Optional[str] = None,
        cloud: Optional[PowerPlatformCloud] = None,
        copilot_agent_type: Optional[AgentType] = None,
        custom_power_platform_cloud: Optional[str] = None,
    ) -> None:
        self.app_client_id = app_client_id or environ.get("APP_CLIENT_ID")
        self.tenant_id = tenant_id or environ.get("TENANT_ID")

        if not self.app_client_id:
            raise ValueError("App Client ID must be provided")
        if not self.tenant_id:
            raise ValueError("Tenant ID must be provided")

        environment_id = environment_id or environ.get("ENVIRONMENT_ID")
        agent_identifier = agent_identifier or environ.get("AGENT_IDENTIFIER")
        cloud = cloud or PowerPlatformCloud[environ.get("CLOUD", "UNKNOWN")]
        copilot_agent_type = copilot_agent_type or AgentType[environ.get("COPILOT_AGENT_TYPE", "PUBLISHED")]
        custom_power_platform_cloud = custom_power_platform_cloud or environ.get("CUSTOM_POWER_PLATFORM_CLOUD", None)

        super().__init__(
            environment_id,
            agent_identifier,
            cloud,
            copilot_agent_type,
            custom_power_platform_cloud,
        )

    def get_msal_token_cache(self, fallback_to_plaintext: bool = True) -> PersistedTokenCache:
        cache_path = environ.get("TOKEN_CACHE_PATH") or Path(__file__).parent / "bin/token_cache.bin"
        persistence = None

        # Note: This sample stores both encrypted persistence and plaintext persistence
        # into same location, therefore their data would likely override with each other.
        try:
            persistence = build_encrypted_persistence(cache_path)
        except Exception:
            # On Linux, encryption exception will be raised during initialization.
            # On Windows and macOS, they won't be detected here,
            # but will be raised during their load() or save().
            if not fallback_to_plaintext:
                raise
            logging.warning("Encryption unavailable. Opting in to plain text.")
            persistence = FilePersistence(cache_path)

        return PersistedTokenCache(persistence)

    def acquire_token(self) -> str:
        cache = self.get_msal_token_cache()
        app = PublicClientApplication(
            self.app_client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            token_cache=cache,
        )

        token_scopes = ["https://api.powerplatform.com/.default"]

        accounts = app.get_accounts()

        if accounts:
            # If so, you could then somehow display these accounts and let end user choose
            chosen = accounts[0]
            result = app.acquire_token_silent(scopes=token_scopes, account=chosen)
        else:
            # At this point, you can save you can update your cache if you are using token caching
            # check result variable, if its None then you should interactively acquire a token
            # So no suitable token exists in cache. Let's get a new one from Microsoft Entra.
            result = app.acquire_token_interactive(scopes=token_scopes)

        if "access_token" in result:
            return result["access_token"]
        logging.error(result.get("error"))
        logging.error(result.get("error_description"))
        logging.error(result.get("correlation_id"))  # You may need this when reporting a bug
        raise Exception("Authentication with the Public AgentApplication failed")


class McsCopilotClient(McsConnectionSettings, CopilotClient):
    def __init__(self, connection_settings: McsConnectionSettings = None, copilot_client: CopilotClient = None) -> None:
        if connection_settings:
            self.connection_settings = connection_settings
        else:
            self.connection_settings = McsConnectionSettings()
        if not copilot_client:
            self.copilot_client = self.create_mcs_client(self.connection_settings)

    def create_mcs_client(self, connection_settings: ConnectionSettings) -> CopilotClient:
        token = connection_settings.acquire_token()
        return CopilotClient(connection_settings, token)

    async def start_conversation_async(self) -> list:
        acts = []
        # Attempt to connect to the copilot studio hosted agent here
        # if successful, this will loop though all events that the Copilot Studio agent sends to the client setup the conversation.
        async for activity in self.copilot_client.start_conversation():
            if activity is not None:
                acts.append(activity)
        return acts

    async def ask_question_async(self, question: str) -> list:
        acts = []
        # Send the user input to the Copilot Studio agent and await the response.
        # In this case we are not sending a conversation ID, as the agent is already connected by "StartConversationAsync", a conversation ID is persisted by the underlying client.
        async for activity in self.copilot_client.ask_question(question):
            if activity is not None:
                acts.append(activity)
        return acts
