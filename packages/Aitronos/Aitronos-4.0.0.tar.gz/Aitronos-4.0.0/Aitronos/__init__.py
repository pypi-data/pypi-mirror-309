"""
Aitronos Package

This package provides an API client for interacting with the Freddy Core API.
"""

from Aitronos.helper import (
    Message,
    MessageRequestPayload,
    StreamEvent,
    is_valid_json,
    extract_json_strings,
    HTTPMethod,
    Config,
    FreddyError,
    perform_request,
)
from Aitronos.AppHive import AppHive, LoginResponse, RefreshToken, AppHiveError
from Aitronos.FreddyApi import FreddyApi
from Aitronos.StreamLine import StreamLine

__all__ = [
    "Aitronos",
    "LoginResponse",
    "RefreshToken",
    "AppHiveError",
    "FreddyApi",
    "StreamLine",
    "Message",
    "MessageRequestPayload",
    "StreamEvent",
    "is_valid_json",
    "FreddyError",
    "HTTPMethod",
    "Config",
    "perform_request",
]


class Aitronos:
    def __init__(self, api_key: str = None, username: str = None, password: str = None):
        """
        Initialize the Aitronos package.

        :param api_key: (Optional) API token for authentication.
        :param username: (Optional) Username or email to log in and retrieve the API token.
        :param password: (Optional) Password to log in and retrieve the API token.
        """
        self._user_token = None
        self.BASE_URL = "https://freddy-api.aitronos.com"

        if api_key and api_key.strip():
            # Use the provided API key
            self._user_token = api_key
        elif username and password and username.strip() and password.strip():
            # Obtain the API key using the credentials
            self._user_token = self._authenticate_and_get_token(username, password)
        else:
            raise ValueError("You must provide either an API key or valid username and password.")

    def _authenticate_and_get_token(self, username: str, password: str) -> str:
        """
        Authenticate the user with their credentials and return the API token.

        :param username: The user's email or username.
        :param password: The user's password.
        :return: The API token.
        """
        from Aitronos.AppHive import Authentication

        # Use the Authentication class to log in and retrieve the token
        auth = Authentication(base_url=self.BASE_URL)
        try:
            response = auth.login(username, password)
        except AppHiveError as e:
            # Propagate the error
            raise e

        # Validate the response structure
        if not isinstance(response, LoginResponse):
            raise AppHiveError(AppHiveError.Type.INVALID_RESPONSE, "Invalid response structure")

        if not response.token or not response.refresh_token or not response.device_id:
            raise AppHiveError(AppHiveError.Type.INVALID_RESPONSE, "Missing required fields in response")

        return response.token

    @property
    def AppHive(self):
        """
        Provides an instance of the AppHive class, initialized with the API token.
        """
        if not self._user_token:
            raise ValueError("User token is not available. Please authenticate first.")
        return AppHive(user_token=self._user_token)

    @property
    def FreddyApi(self):
        """
        Provides an instance of the FreddyApi class, initialized with the API token.
        """
        if not self._user_token:
            raise ValueError("User token is not available. Please authenticate first.")
        return FreddyApi(self._user_token)

    @property
    def AssistantMessaging(self):
        """
        Provides an instance of the AssistantMessaging class, initialized with the API token.
        """
        if not self._user_token:
            raise ValueError("User token is not available. Please authenticate first.")
        return FreddyApi.AssistantMessaging(self._user_token)
