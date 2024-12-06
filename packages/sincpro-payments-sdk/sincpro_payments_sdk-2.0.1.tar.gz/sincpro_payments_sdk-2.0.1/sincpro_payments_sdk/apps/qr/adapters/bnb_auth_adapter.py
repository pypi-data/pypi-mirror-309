"""Adapter for BNB Auth API."""

from enum import StrEnum

from sincpro_payments_sdk.apps.qr.domain import QRBNBCredentials
from sincpro_payments_sdk.shared.client_api import ClientAPI


class BNBAuthRoutes(StrEnum):
    """Routes for BNB Auth API."""

    JSON_WEB_TOKEN = "/auth/token"


class BNBAuthAdapter(ClientAPI):

    def __init__(self):
        self.ssl = "https://"
        self.host = "test.bnb.com.bo/ClientAuthentication.API/api/v1"
        super().__init__(self.base_url)

    @property
    def base_url(self):
        """Get the base URL for the CyberSource API."""
        return f"{self.ssl}{self.host}"

    def get_jwt(self, body: QRBNBCredentials) -> str:
        """Get JWT from BNB."""
        response = self.execute_request(
            BNBAuthRoutes.JSON_WEB_TOKEN,
            "POST",
            data={"accountId": body.account_id, "authorizationId": body.authorization_id},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        dict_response = response.json()

        return dict_response.get("message")
