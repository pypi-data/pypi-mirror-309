# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .subscription import (
    SubscriptionResource,
    AsyncSubscriptionResource,
    SubscriptionResourceWithRawResponse,
    AsyncSubscriptionResourceWithRawResponse,
    SubscriptionResourceWithStreamingResponse,
    AsyncSubscriptionResourceWithStreamingResponse,
)
from ...._base_client import make_request_options
from ....types.messages import sms_outbound_params
from ....types.messages.resource_reference import ResourceReference

__all__ = ["SMSResource", "AsyncSMSResource"]


class SMSResource(SyncAPIResource):
    @cached_property
    def subscription(self) -> SubscriptionResource:
        return SubscriptionResource(self._client)

    @cached_property
    def with_raw_response(self) -> SMSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#accessing-raw-response-data-eg-headers
        """
        return SMSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SMSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#with_streaming_response
        """
        return SMSResourceWithStreamingResponse(self)

    def outbound(
        self,
        *,
        client_correlator_id: str,
        message: str,
        receiver_address: List[str],
        service_code: str,
        keyword: str | NotGiven = NOT_GIVEN,
        request_delivery_receipt: bool | NotGiven = NOT_GIVEN,
        sender_address: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResourceReference:
        """
        This interface is used to send an SMS to the specified receiverAddress.

        Args:
          client_correlator_id: It uniquely identifies the request.This can be alphanumeric or numeric depending
              on the consumers id pattern .

          message: The message being sent. The standard limit of the size of the message is 160 for
              English texts and about 250 to 300 characters for french related texts.

          receiver_address: This an array of the subscriber MSISDN(s) that the SMS is being sent to. The
              value is represented as International ITU-T E.164. If more than one address is
              used the values will be comma separated.Thare are no limits to the length of the
              array but a sizable amount of 20 to 30 is expected for optimal delivery to
              recipients.

          service_code: This is the short code that is provided by the api consumer and is approved by
              the opco for sending messages on behalf of a 3pp. This field is mandatory and if
              a senderAddress is used rather than the serviceCode , then the senderAddress
              value must be passed as well to this field,this will ensure that the messages
              are sent using the senderAddress.

          keyword: The keyword field is used in cases where the partner needs to share the short
              code and the partner had already subscribed with this keyword for Delivery
              Receipts via the subscriptions endpoint. The keyword field will then be used to
              send an outbound request to indicate that this request uses a shared short code
              and the Delivery receipt will be sent to the endpoint that was registered with
              this keyword .
              `Currently this is only used and was requested by the Nigeria opco `

          request_delivery_receipt: This is used to indicate whether the 3pp needs a delivery report or not. By
              default this is set to false . When set to true the consumer should ensure that
              they must have subscribed for delivery receipts or mobile originating messages
              using the subscriptions endpoints below .

          sender_address: This is the sender address the recipients will see on their devices as the
              sender of the message. This is alphanumeric. This field is optional when it has
              a value it takes precedence over the serviceCode and is used to send messages
              rather than using serviceCode.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/messages/sms/outbound",
            body=maybe_transform(
                {
                    "client_correlator_id": client_correlator_id,
                    "message": message,
                    "receiver_address": receiver_address,
                    "service_code": service_code,
                    "keyword": keyword,
                    "request_delivery_receipt": request_delivery_receipt,
                    "sender_address": sender_address,
                },
                sms_outbound_params.SMSOutboundParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResourceReference,
        )


class AsyncSMSResource(AsyncAPIResource):
    @cached_property
    def subscription(self) -> AsyncSubscriptionResource:
        return AsyncSubscriptionResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSMSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#accessing-raw-response-data-eg-headers
        """
        return AsyncSMSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSMSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#with_streaming_response
        """
        return AsyncSMSResourceWithStreamingResponse(self)

    async def outbound(
        self,
        *,
        client_correlator_id: str,
        message: str,
        receiver_address: List[str],
        service_code: str,
        keyword: str | NotGiven = NOT_GIVEN,
        request_delivery_receipt: bool | NotGiven = NOT_GIVEN,
        sender_address: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResourceReference:
        """
        This interface is used to send an SMS to the specified receiverAddress.

        Args:
          client_correlator_id: It uniquely identifies the request.This can be alphanumeric or numeric depending
              on the consumers id pattern .

          message: The message being sent. The standard limit of the size of the message is 160 for
              English texts and about 250 to 300 characters for french related texts.

          receiver_address: This an array of the subscriber MSISDN(s) that the SMS is being sent to. The
              value is represented as International ITU-T E.164. If more than one address is
              used the values will be comma separated.Thare are no limits to the length of the
              array but a sizable amount of 20 to 30 is expected for optimal delivery to
              recipients.

          service_code: This is the short code that is provided by the api consumer and is approved by
              the opco for sending messages on behalf of a 3pp. This field is mandatory and if
              a senderAddress is used rather than the serviceCode , then the senderAddress
              value must be passed as well to this field,this will ensure that the messages
              are sent using the senderAddress.

          keyword: The keyword field is used in cases where the partner needs to share the short
              code and the partner had already subscribed with this keyword for Delivery
              Receipts via the subscriptions endpoint. The keyword field will then be used to
              send an outbound request to indicate that this request uses a shared short code
              and the Delivery receipt will be sent to the endpoint that was registered with
              this keyword .
              `Currently this is only used and was requested by the Nigeria opco `

          request_delivery_receipt: This is used to indicate whether the 3pp needs a delivery report or not. By
              default this is set to false . When set to true the consumer should ensure that
              they must have subscribed for delivery receipts or mobile originating messages
              using the subscriptions endpoints below .

          sender_address: This is the sender address the recipients will see on their devices as the
              sender of the message. This is alphanumeric. This field is optional when it has
              a value it takes precedence over the serviceCode and is used to send messages
              rather than using serviceCode.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/messages/sms/outbound",
            body=await async_maybe_transform(
                {
                    "client_correlator_id": client_correlator_id,
                    "message": message,
                    "receiver_address": receiver_address,
                    "service_code": service_code,
                    "keyword": keyword,
                    "request_delivery_receipt": request_delivery_receipt,
                    "sender_address": sender_address,
                },
                sms_outbound_params.SMSOutboundParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResourceReference,
        )


class SMSResourceWithRawResponse:
    def __init__(self, sms: SMSResource) -> None:
        self._sms = sms

        self.outbound = to_raw_response_wrapper(
            sms.outbound,
        )

    @cached_property
    def subscription(self) -> SubscriptionResourceWithRawResponse:
        return SubscriptionResourceWithRawResponse(self._sms.subscription)


class AsyncSMSResourceWithRawResponse:
    def __init__(self, sms: AsyncSMSResource) -> None:
        self._sms = sms

        self.outbound = async_to_raw_response_wrapper(
            sms.outbound,
        )

    @cached_property
    def subscription(self) -> AsyncSubscriptionResourceWithRawResponse:
        return AsyncSubscriptionResourceWithRawResponse(self._sms.subscription)


class SMSResourceWithStreamingResponse:
    def __init__(self, sms: SMSResource) -> None:
        self._sms = sms

        self.outbound = to_streamed_response_wrapper(
            sms.outbound,
        )

    @cached_property
    def subscription(self) -> SubscriptionResourceWithStreamingResponse:
        return SubscriptionResourceWithStreamingResponse(self._sms.subscription)


class AsyncSMSResourceWithStreamingResponse:
    def __init__(self, sms: AsyncSMSResource) -> None:
        self._sms = sms

        self.outbound = async_to_streamed_response_wrapper(
            sms.outbound,
        )

    @cached_property
    def subscription(self) -> AsyncSubscriptionResourceWithStreamingResponse:
        return AsyncSubscriptionResourceWithStreamingResponse(self._sms.subscription)
