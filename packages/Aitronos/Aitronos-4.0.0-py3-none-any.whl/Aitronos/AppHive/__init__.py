from Aitronos.AppHive.helper import AppHiveError
from Aitronos.AppHive.authentication import Authentication, LoginResponse, RefreshToken
from Aitronos.AppHive.UserManagement import Address, ProfileImage, UpdateUserProfileRequest, UserManagement

__all__ = [
    "AppHive",
    "LoginResponse",
    "RefreshToken",
    "AppHiveError",
    "Address",
    "ProfileImage",
    "UpdateUserProfileRequest",
]


class AppHive:
    """
    A Python class for interacting with the AppHive API.
    """

    BASE_URL = "https://freddy-api.aitronos.com"

    def __init__(self, user_token: str = None, username: str = None, password: str = None):
        """
        Initialize the AppHive class with either a user token or user credentials.

        :param user_token: The API token for authentication (optional).
        :param username: The user's email or username for login (optional).
        :param password: The user's password for login (optional).
        :raises ValueError: If neither a user token nor valid credentials are provided.
        """
        if user_token:
            self._user_token = user_token
        elif username and password:
            self._user_token = self._authenticate_and_get_token(username, password)
        else:
            raise ValueError("You must provide either an API token or valid username and password.")

    @property
    def authentication(self) -> Authentication:
        """
        Provides access to the Authentication class.

        :return: An instance of the Authentication class.
        """
        return Authentication(self.BASE_URL)

    @property
    def user_management(self) -> UserManagement:
        """
        Provides access to the UserManagement class.

        :return: An instance of the UserManagement class.
        """
        return UserManagement(self.BASE_URL, self.user_token)

    @property
    def user_token(self) -> str:
        """
        Getter for the user token.

        :return: The user token as a string.
        """
        return self._user_token

    @user_token.setter
    def user_token(self, value: str):
        """
        Setter for the user token.

        :param value: The new user token.
        :raises ValueError: If the user token is empty.
        """
        if not value:
            raise ValueError("AppHive API Key cannot be empty")
        self._user_token = value

    def _authenticate_and_get_token(self, username: str, password: str) -> str:
        """
        Authenticate the user with their credentials and retrieve the API token.

        :param username: The user's email or username.
        :param password: The user's password.
        :return: The API token as a string.
        :raises AppHiveError: If authentication fails.
        """
        auth = Authentication(self.BASE_URL)
        response = auth.login(username, password)

        if isinstance(response, LoginResponse):
            return response.token
        elif isinstance(response, AppHiveError):
            raise ValueError(f"Failed to authenticate: {response.description}")
        else:
            raise ValueError("Unexpected error during authentication.")
