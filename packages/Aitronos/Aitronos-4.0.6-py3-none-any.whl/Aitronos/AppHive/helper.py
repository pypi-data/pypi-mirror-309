import json
from typing import Optional, Dict, Any, Union
import requests


# MARK: - AppHiveError Class
class AppHiveError(Exception):
    class Type:
        NETWORK_ISSUE = "networkIssue"
        INVALID_RESPONSE = "invalidResponse"
        HTTP_ERROR = "httpError"
        DECODING_ERROR = "decodingError"
        NO_DATA = "noData"

    def __init__(self, error_type: str, description: Optional[str] = None):
        self.error_type = error_type
        self.description = description or ""

    def __str__(self):
        return f"{self.error_type}: {self.description}"


# MARK: - perform_request Helper Function
def perform_request(
        endpoint: str,
        method: str,
        base_url: str,
        body: Optional[Dict[str, Any]] = None,
        empty_response: bool = False,
        api_key: Optional[str] = None
) -> Union[Dict[str, Any], AppHiveError]:
    """
    Perform an HTTP request and return the parsed response or an error.
    """
    url = f"{base_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
    }

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body
        )

        if not (200 <= response.status_code < 300):
            try:
                error_details = response.json().get("error", "Unknown Error")
            except json.JSONDecodeError:
                error_details = response.text
            return AppHiveError(AppHiveError.Type.HTTP_ERROR, f"HTTP {response.status_code}: {error_details}")

        if empty_response:
            return {}
        try:
            return response.json()
        except json.JSONDecodeError:
            return AppHiveError(AppHiveError.Type.DECODING_ERROR, "Invalid JSON in response")

    except requests.RequestException as e:
        return AppHiveError(AppHiveError.Type.NETWORK_ISSUE, str(e))
