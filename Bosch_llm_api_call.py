

import requests
from typing import Dict, List, Any

class BoschApiClient:
    """
    Client wrapper for obtaining a token using `client_credentials` and calling the chat messages API.
    """

    def __init__(
        self,
        oauth2_client_id: str,
        oauth2_client_secret: str,
        tenant_or_directory_id: str,
        api_url: str = "https://aigc.bosch.com.cn/llmservice/api/v1/chat/messages",
        model_name: str = "gpt4o-mini",
        temperature: float = 0.1
    ):
        """
        :param oauth2_client_id: Client ID of the Azure App Registration
        :param oauth2_client_secret: Client Secret of the Azure App Registration
        :param tenant_or_directory_id: Typically your tenant ID or directory ID
        :param api_host: Domain of the chat messages API, e.g., "https://aigc.bosch.com.cn/llmservice/api/v1/chat/messages"
        :param model_name: Default model name for sending requests
        :param temperature: Default temperature for sending requests
        """
        self.oauth2_client_id = oauth2_client_id
        self.oauth2_client_secret = oauth2_client_secret
        self.tenant_or_directory_id = tenant_or_directory_id
        self.api_url = api_url
        self.model_name = model_name
        self.temperature = temperature

    def get_access_token(self) -> str:
        """
        Get Azure AD Token from Client Credentials Flow
        """
        url = f"https://login.microsoftonline.com/{self.tenant_or_directory_id}/oauth2/v2.0/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.oauth2_client_id,
            "client_secret": self.oauth2_client_secret,
            "scope": f"{self.oauth2_client_id}/.default",
            "grant_type": "client_credentials"
        }
        resp = requests.post(url, headers=headers, data=data, verify=False)
        resp.raise_for_status()
        token_json = resp.json()
        return token_json["access_token"]

    def chat(
        self, 
        messages: List[Dict[str, str]],
        model_name: str = None,
        temperature: float = None
    ) -> Dict[str, Any]:
        """
        Calls the `/llmservice/api/v1/chat/messages` endpoint to send chat messages.

        :param messages: In the format [{"role": "user", "content": "hello"}]
        :param model_name: Optional, specifies the model; uses the default if not provided
        :param temperature: Optional, specifies the temperature; uses the default if not provided
        :return: JSON structure returned by the API
        """
        access_token = self.get_access_token()
        url = self.api_url

        payload = {
            "messages": messages,
            "model": model_name if model_name else self.model_name,
            "temperature": temperature if temperature is not None else self.temperature
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        resp = requests.post(url, json=payload, headers=headers, verify=False)
        resp.raise_for_status()
        return resp.json()