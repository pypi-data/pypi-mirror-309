# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SubscriptionResponse", "Data"]


class Data(BaseModel):
    subscription_id: Optional[str] = FieldInfo(alias="subscriptionId", default=None)
    """Unique identifier for the subscription"""


class SubscriptionResponse(BaseModel):
    data: Data

    status_code: str = FieldInfo(alias="statusCode")
    """
    This is the MADAPI Canonical Error Code (it is 4 characters long and it is not
    the HTTP Status Code which is 3 characters long). Back-end system errors are
    mapped to specific canonical error codes which are returned. More information on
    these mappings can be found on the MADAPI Confluence Page 'Response Codes'
    """

    status_message: str = FieldInfo(alias="statusMessage")
    """
    More details and corrective actions related to the error which can be shown to a
    client.
    """

    transaction_id: str = FieldInfo(alias="transactionId")
    """MADAPI generated Id to include for tracing requests"""
