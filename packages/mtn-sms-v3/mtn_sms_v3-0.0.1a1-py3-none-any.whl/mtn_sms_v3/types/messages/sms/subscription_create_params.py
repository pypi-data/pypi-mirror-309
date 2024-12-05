# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SubscriptionCreateParams"]


class SubscriptionCreateParams(TypedDict, total=False):
    callback_url: Required[Annotated[str, PropertyInfo(alias="callbackUrl")]]
    """
    This is the callback URL that will be invoked when a Mobile originating or
    Delivery Receipt message is sent by a Subscriber to the configured short code .
    """

    service_code: Required[Annotated[str, PropertyInfo(alias="serviceCode")]]
    """
    This is the service code that is being registered for Mobile originating and
    delivery receipt calls
    """

    target_system: Required[Annotated[str, PropertyInfo(alias="targetSystem")]]
    """
    Target system indicates the name of the system that this Mobile originating
    request will be sent to.
    """

    delivery_report_url: Annotated[str, PropertyInfo(alias="deliveryReportUrl")]
    """
    This is the URL where the delivery receipts for messages sent with the
    /messages/sms/outbound endpoint will be sent. The messages will be sent to the
    deliveryReportUrl if requestDeliveryReceipt is set to true , by default it is
    false when sending an outbound message.
    """

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]
