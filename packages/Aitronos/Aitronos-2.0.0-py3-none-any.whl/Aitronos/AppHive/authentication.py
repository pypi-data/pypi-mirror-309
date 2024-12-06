from dataclasses import dataclass
from typing import Union
from .helper import perform_request, AppHiveError


# MARK: - Data Models
@dataclass
class RefreshToken:
    token: str
    expiry: str


@dataclass
class LoginResponse:
    token: str
    refresh_token: RefreshToken
    device_id: str


# MARK: - Authentication Class
class Authentication:
    def __init__(self, base_url: str):
        """
        Initialize the Authentication class with a base URL.

        :param base_url: The base URL for the API.
        """
        self.base_url = base_url

    def login(self, username_email: str, password: str) -> LoginResponse:
        """
        Synchronous user authentication.

        :param username_email: The user's email or username.
        :param password: The user's password.
        :return: A LoginResponse object containing the user's token, refresh token, and device ID.
        :raises AppHiveError: If the login process encounters an error.
        """
        endpoint = "/auth/login"
        request_body = {"emailOrUserName": username_email, "password": password}

        # Perform the API request
        result = perform_request(
            endpoint=endpoint,
            method="POST",
            base_url=self.base_url,
            body=request_body,
            empty_response=False,
        )

        # Handle errors
        if isinstance(result, AppHiveError):
            raise result

        # Parse and return the response
        try:
            refresh_token = RefreshToken(
                token=result["refreshToken"]["token"],
                expiry=result["refreshToken"]["expiry"]
            )
            return LoginResponse(
                token=result["token"],
                refresh_token=refresh_token,
                device_id=result["deviceId"]
            )
        except KeyError as e:
            raise AppHiveError(AppHiveError.Type.INVALID_RESPONSE, f"Missing key: {str(e)}")