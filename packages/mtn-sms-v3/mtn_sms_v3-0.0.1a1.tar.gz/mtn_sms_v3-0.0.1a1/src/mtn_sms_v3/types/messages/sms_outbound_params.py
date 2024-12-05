# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["SMSOutboundParams"]


class SMSOutboundParams(TypedDict, total=False):
    client_correlator_id: Required[Annotated[str, PropertyInfo(alias="clientCorrelatorId")]]
    """
    It uniquely identifies the request.This can be alphanumeric or numeric depending
    on the consumers id pattern .
    """

    message: Required[str]
    """The message being sent.

    The standard limit of the size of the message is 160 for English texts and about
    250 to 300 characters for french related texts.
    """

    receiver_address: Required[Annotated[List[str], PropertyInfo(alias="receiverAddress")]]
    """This an array of the subscriber MSISDN(s) that the SMS is being sent to.

    The value is represented as International ITU-T E.164. If more than one address
    is used the values will be comma separated.Thare are no limits to the length of
    the array but a sizable amount of 20 to 30 is expected for optimal delivery to
    recipients.
    """

    service_code: Required[Annotated[str, PropertyInfo(alias="serviceCode")]]
    """
    This is the short code that is provided by the api consumer and is approved by
    the opco for sending messages on behalf of a 3pp. This field is mandatory and if
    a senderAddress is used rather than the serviceCode , then the senderAddress
    value must be passed as well to this field,this will ensure that the messages
    are sent using the senderAddress.
    """

    keyword: str
    """
    The keyword field is used in cases where the partner needs to share the short
    code and the partner had already subscribed with this keyword for Delivery
    Receipts via the subscriptions endpoint. The keyword field will then be used to
    send an outbound request to indicate that this request uses a shared short code
    and the Delivery receipt will be sent to the endpoint that was registered with
    this keyword .
    `Currently this is only used and was requested by the Nigeria opco `
    """

    request_delivery_receipt: Annotated[bool, PropertyInfo(alias="requestDeliveryReceipt")]
    """This is used to indicate whether the 3pp needs a delivery report or not.

    By default this is set to false . When set to true the consumer should ensure
    that they must have subscribed for delivery receipts or mobile originating
    messages using the subscriptions endpoints below .
    """

    sender_address: Annotated[str, PropertyInfo(alias="senderAddress")]
    """
    This is the sender address the recipients will see on their devices as the
    sender of the message. This is alphanumeric. This field is optional when it has
    a value it takes precedence over the serviceCode and is used to send messages
    rather than using serviceCode.
    """
