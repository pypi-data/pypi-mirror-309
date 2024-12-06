from dataclasses import dataclass
from typing import Dict, Any, Optional
from .helper import perform_request, AppHiveError


@dataclass
class Address:
    full_name: str
    street: str
    post_code: str
    city: str
    country: int
    phone_number: str


@dataclass
class ProfileImage:
    background: str
    image: str


@dataclass
class UpdateUserProfileRequest:
    full_name: str
    last_name: str
    user_name: str
    email: str
    address: Address
    profile_image: ProfileImage
    birthday: str
    gender: int
    country: int
    password: str


class UserManagement:
    """
    A class for managing user-related operations, such as checking username duplication and fetching user profiles.
    """

    def __init__(self, base_url: str, user_token: str):
        """
        Initialize the UserManagement class.

        :param base_url: The base URL for the API.
        :param user_token: The authentication token for API access.
        """
        self.base_url = base_url
        self.user_token = user_token

    def check_username_duplication(self, user_id: int, username: str) -> bool:
        """
        Checks whether the new username is already taken.
        """
        endpoint = "/v1/user/username/checkforduplicate"
        request_body = {"userId": user_id, "userName": username}

        result = perform_request(
            endpoint=endpoint,
            method="POST",
            base_url=self.base_url,
            body=request_body,
            empty_response=False,
            api_key=self.user_token,
        )

        if isinstance(result, AppHiveError):
            raise result

        if isinstance(result, bool):
            return result

        raise AppHiveError(
            AppHiveError.Type.INVALID_RESPONSE,
            "Invalid response format from server",
        )

    def get_basic_user_profile(self) -> Dict[str, Any]:
        """
        Fetches the basic profile information of the currently logged-in user.
        """
        endpoint = "/v1/user"

        result = perform_request(
            endpoint=endpoint,
            method="GET",
            base_url=self.base_url,
            empty_response=False,
            api_key=self.user_token,
        )

        if isinstance(result, AppHiveError):
            raise result

        return result

    def get_detailed_user_profile(self) -> Dict[str, Any]:
        """
        Fetches the detailed profile information of the currently logged-in user.
        """
        endpoint = "/v1/user/profile"

        result = perform_request(
            endpoint=endpoint,
            method="GET",
            base_url=self.base_url,
            empty_response=False,
            api_key=self.user_token,
        )

        if isinstance(result, AppHiveError):
            raise result

        return result

    def register_user(self, email: str, password: str, full_name: str) -> Dict[str, Any]:
        """
        Registers a new user.
        """
        endpoint = "/v1/user/register"
        request_body = {
            "email": email,
            "password": password,
            "fullName": full_name,
        }

        result = perform_request(
            endpoint=endpoint,
            method="POST",
            base_url=self.base_url,
            body=request_body,
            empty_response=False,
        )

        if isinstance(result, AppHiveError):
            raise result

        verification_response = result.get("verificationResponse")
        if verification_response and isinstance(verification_response, dict):
            return verification_response

        raise AppHiveError(
            AppHiveError.Type.INVALID_RESPONSE,
            "Invalid or incomplete verification response",
        )

    def update_username(self, user_id: int, user_name: str) -> bool:
        """
        Updates the unique username for a user.
        """
        endpoint = f"/v1/user/{user_id}/username/update"
        request_body = {
            "userId": user_id,
            "userName": user_name,
        }

        result = perform_request(
            endpoint=endpoint,
            method="PUT",
            base_url=self.base_url,
            body=request_body,
            empty_response=False,
            api_key=self.user_token,
        )

        if isinstance(result, AppHiveError):
            raise result

        if isinstance(result, bool):
            return result

        raise AppHiveError(
            AppHiveError.Type.INVALID_RESPONSE,
            "Unexpected response format from server",
        )

    def update_user_profile(self, profile_data: UpdateUserProfileRequest) -> None:
        """
        Updates the user's profile data.
        """
        endpoint = "/v1/user"
        profile_dict = {
            "fullName": profile_data.full_name,
            "lastName": profile_data.last_name,
            "userName": profile_data.user_name,
            "email": profile_data.email,
            "address": {
                "fullName": profile_data.address.full_name,
                "street": profile_data.address.street,
                "postCode": profile_data.address.post_code,
                "city": profile_data.address.city,
                "country": profile_data.address.country,
                "phoneNumber": profile_data.address.phone_number,
            },
            "profileImage": {
                "background": profile_data.profile_image.background,
                "image": profile_data.profile_image.image,
            },
            "birthday": profile_data.birthday,
            "gender": profile_data.gender,
            "country": profile_data.country,
            "password": profile_data.password,
        }

        result = perform_request(
            endpoint=endpoint,
            method="POST",
            base_url=self.base_url,
            body=profile_dict,
            empty_response=True,
            api_key=self.user_token,
        )

        if isinstance(result, AppHiveError):
            raise result
