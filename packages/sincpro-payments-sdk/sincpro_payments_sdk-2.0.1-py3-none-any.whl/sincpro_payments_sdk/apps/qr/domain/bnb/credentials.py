"""BNB Credentials setup for QR API."""

from sincpro_payments_sdk.shared.pydantic import BaseModel


class QRBNBCredentials(BaseModel):
    """Credentials for BNB QR API."""

    account_id: str
    authorization_id: str
    jwt_token: str | None = None
