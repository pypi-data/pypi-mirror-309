# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SubscriptionUpdateParams"]


class SubscriptionUpdateParams(TypedDict, total=False):
    callback_url: Annotated[str, PropertyInfo(alias="callbackUrl")]
    """This is the callback URL"""

    delivery_report_url: Annotated[str, PropertyInfo(alias="deliveryReportUrl")]
    """This is the delivery URL"""

    keywords: List[str]
    """Keywords applies to a shared short code .

    This is applicable only for the Nigeria opco.
    """

    service_code: Annotated[str, PropertyInfo(alias="serviceCode")]
    """Service code that is being shared"""

    target_system: Annotated[str, PropertyInfo(alias="targetSystem")]

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]
