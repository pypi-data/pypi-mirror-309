import logging
import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union, Callable
import requests
import re
from Aitronos.helper import Message, MessageRequestPayload, StreamEvent, is_valid_json  # Use helpers from Aitronos

# Set up basic logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class FreddyApi:
    def __init__(self, user_token: str):
        if not user_token:
            raise ValueError("AppHive API Key cannot be empty")
        self._user_token = user_token
        self._base_url = "https://freddy-api.aitronos.com"

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def user_token(self) -> str:
        return self._user_token

    @user_token.setter
    def user_token(self, value: str):
        if not value:
            raise ValueError("AppHive API Key cannot be empty")
        self._user_token = value

    class AssistantMessaging:
        JSON_PATTERN = re.compile(r'\{[^{}]*\}|\[[^\[\]]*\]')

        def __init__(self, user_token: str):
            self.user_token = user_token
            self.base_url = "https://freddy-api.aitronos.com/v1"
            self.session = requests.Session()
            self.rate_limit_reached = False

        def create_stream(self, payload: MessageRequestPayload, callback: Callable[[StreamEvent], None]) -> None:
            """Creates a streaming request to the run-stream endpoint."""
            url = f"{self.base_url}/messages/run-stream"
            headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }
            data = payload.to_dict()

            try:
                response = self.session.post(url, json=data, headers=headers, stream=True)
                response.raise_for_status()

                buffer = ""
                for chunk in response.iter_content(decode_unicode=True):
                    buffer += chunk.decode('utf-8')
                    matches = list(re.finditer(self.JSON_PATTERN, buffer))

                    for match in matches:
                        json_str = match.group()
                        try:
                            json_data = json.loads(json_str)
                            event = StreamEvent.from_json(json_data)
                            callback(event)
                        except json.JSONDecodeError as e:
                            log.error(f"Failed to decode JSON: {e}")

                    buffer = buffer[matches[-1].end():] if matches else buffer

            except requests.RequestException as e:
                log.error(f"Request to {url} failed. Error details: {e}")
                raise Exception(f"Network or connection error while making request to {url}. Details: {e}")

        def create_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
            """Sends a non-streaming POST request to the run-create endpoint."""
            if self.rate_limit_reached:
                log.error("Rate limit reached. Please try again later.")
                raise Exception("Rate limit reached, please try again later.")

            url = f"{self.base_url}/messages/run-create"
            headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }

            try:
                # Convert the payload to a dictionary
                data = payload.to_dict()

                # Log the payload for debugging
                log.debug(f"Payload for request: {data}")

                # Perform the POST request
                response = self.session.post(url, headers=headers, json=data)
                response.raise_for_status()
                self.rate_limit_reached = True
                return response.json()

            except requests.RequestException as e:
                log.error(f"Error during API request to {url}: {e}")
                raise Exception(f"Network or connection error while making request to {url}. Details: {e}")

        def check_run_status(self, run_key: str, thread_key: str, organization_id: int) -> str:
            """Checks the status of a previously created run."""
            url = f"{self.base_url}/messages/run-status"
            headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "organization_id": organization_id,
                "thread_key": thread_key,
                "run_key": run_key
            }

            try:
                response = self.session.get(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json().get("runStatus", "unknown")

            except requests.RequestException as e:
                log.error(f"Error while checking run status at {url}: {e}")
                return "error"

        def get_run_response(self, organization_id: int, thread_key: str) -> Union[Dict, None]:
            """Gets the response of a completed run."""
            url = f"{self.base_url}/messages/run-response"
            headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }
            payload = {"organization_id": organization_id, "thread_key": thread_key}

            try:
                response = self.session.get(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                log.error(f"Error occurred while making request to {url}. Details: {e}")
                raise Exception(f"Error occurred while making request to {url}. Details: {e}")

        def execute_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
            """Executes a non-streaming run request."""
            url = f"{self.base_url}/messages/run-stream"
            headers = {
                "Authorization": f"Bearer {self.user_token}",
                "Content-Type": "application/json"
            }
            data = payload.to_dict()
            data["stream"] = False

            try:
                response = self.session.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                log.error(f"Error occurred while making request to {url}. Details: {e}")
                raise Exception(f"Network or connection error during API request. Details: {e}")