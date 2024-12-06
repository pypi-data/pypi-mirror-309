"""Res api adapter."""

from sincpro_payments_sdk.shared.client_api import ClientAPI


class QRBNBApiAdapter(ClientAPI):

    def __init__(self):
        self.ssl = "https://"
        self.host = "test.bnb.com.bo/QRSimple.API/api/v1"
        super().__init__(self.base_url)

    @property
    def base_url(self):
        """Get the base URL for the CyberSource API."""
        return f"{self.ssl}{self.host}"
