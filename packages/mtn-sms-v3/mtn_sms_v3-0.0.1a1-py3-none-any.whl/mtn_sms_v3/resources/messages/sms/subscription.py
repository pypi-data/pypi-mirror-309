# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    strip_not_given,
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
from ...._base_client import make_request_options
from ....types.messages.sms import subscription_create_params, subscription_update_params
from ....types.messages.sms.subscription_response import SubscriptionResponse
from ....types.messages.sms.subscription_delete_response import SubscriptionDeleteResponse

__all__ = ["SubscriptionResource", "AsyncSubscriptionResource"]


class SubscriptionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SubscriptionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#accessing-raw-response-data-eg-headers
        """
        return SubscriptionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SubscriptionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#with_streaming_response
        """
        return SubscriptionResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        callback_url: str,
        service_code: str,
        target_system: str,
        delivery_report_url: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubscriptionResponse:
        """
        This is the interface used to register callbackUrl (For Mobile originating
        Messages ) and deliveryReportUrl (for Delivery Receipts ) for a
        shortCode/serviceCode/senderAddress.

        Args:
          callback_url: This is the callback URL that will be invoked when a Mobile originating or
              Delivery Receipt message is sent by a Subscriber to the configured short code .

          service_code: This is the service code that is being registered for Mobile originating and
              delivery receipt calls

          target_system: Target system indicates the name of the system that this Mobile originating
              request will be sent to.

          delivery_report_url: This is the URL where the delivery receipts for messages sent with the
              /messages/sms/outbound endpoint will be sent. The messages will be sent to the
              deliveryReportUrl if requestDeliveryReceipt is set to true , by default it is
              false when sending an outbound message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return self._post(
            "/messages/sms/subscription",
            body=maybe_transform(
                {
                    "callback_url": callback_url,
                    "service_code": service_code,
                    "target_system": target_system,
                    "delivery_report_url": delivery_report_url,
                },
                subscription_create_params.SubscriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResponse,
        )

    def update(
        self,
        subscription_id: str,
        *,
        callback_url: str | NotGiven = NOT_GIVEN,
        delivery_report_url: str | NotGiven = NOT_GIVEN,
        keywords: List[str] | NotGiven = NOT_GIVEN,
        service_code: str | NotGiven = NOT_GIVEN,
        target_system: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubscriptionResponse:
        """
        Patch or update an existing subscription based on the subscriptionId , The
        subscriptionId is generated at the point of registering a short code for Mobile
        originating messages or Delivery Receipts with the /messages/sms/subscription
        endpoint above.

        Args:
          callback_url: This is the callback URL

          delivery_report_url: This is the delivery URL

          keywords: Keywords applies to a shared short code . This is applicable only for the
              Nigeria opco.

          service_code: Service code that is being shared

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return self._patch(
            f"/messages/sms/subscription/{subscription_id}",
            body=maybe_transform(
                {
                    "callback_url": callback_url,
                    "delivery_report_url": delivery_report_url,
                    "keywords": keywords,
                    "service_code": service_code,
                    "target_system": target_system,
                },
                subscription_update_params.SubscriptionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResponse,
        )

    def delete(
        self,
        subscription_id: str,
        *,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubscriptionDeleteResponse:
        """
        This interface will stop our systems from sending Mobile originating messages
        and Delivery status reports to the provided delivery report and callback urls
        for a configured serviceCode.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return self._delete(
            f"/messages/sms/subscription/{subscription_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionDeleteResponse,
        )


class AsyncSubscriptionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSubscriptionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#accessing-raw-response-data-eg-headers
        """
        return AsyncSubscriptionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSubscriptionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#with_streaming_response
        """
        return AsyncSubscriptionResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        callback_url: str,
        service_code: str,
        target_system: str,
        delivery_report_url: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubscriptionResponse:
        """
        This is the interface used to register callbackUrl (For Mobile originating
        Messages ) and deliveryReportUrl (for Delivery Receipts ) for a
        shortCode/serviceCode/senderAddress.

        Args:
          callback_url: This is the callback URL that will be invoked when a Mobile originating or
              Delivery Receipt message is sent by a Subscriber to the configured short code .

          service_code: This is the service code that is being registered for Mobile originating and
              delivery receipt calls

          target_system: Target system indicates the name of the system that this Mobile originating
              request will be sent to.

          delivery_report_url: This is the URL where the delivery receipts for messages sent with the
              /messages/sms/outbound endpoint will be sent. The messages will be sent to the
              deliveryReportUrl if requestDeliveryReceipt is set to true , by default it is
              false when sending an outbound message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return await self._post(
            "/messages/sms/subscription",
            body=await async_maybe_transform(
                {
                    "callback_url": callback_url,
                    "service_code": service_code,
                    "target_system": target_system,
                    "delivery_report_url": delivery_report_url,
                },
                subscription_create_params.SubscriptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResponse,
        )

    async def update(
        self,
        subscription_id: str,
        *,
        callback_url: str | NotGiven = NOT_GIVEN,
        delivery_report_url: str | NotGiven = NOT_GIVEN,
        keywords: List[str] | NotGiven = NOT_GIVEN,
        service_code: str | NotGiven = NOT_GIVEN,
        target_system: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubscriptionResponse:
        """
        Patch or update an existing subscription based on the subscriptionId , The
        subscriptionId is generated at the point of registering a short code for Mobile
        originating messages or Delivery Receipts with the /messages/sms/subscription
        endpoint above.

        Args:
          callback_url: This is the callback URL

          delivery_report_url: This is the delivery URL

          keywords: Keywords applies to a shared short code . This is applicable only for the
              Nigeria opco.

          service_code: Service code that is being shared

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return await self._patch(
            f"/messages/sms/subscription/{subscription_id}",
            body=await async_maybe_transform(
                {
                    "callback_url": callback_url,
                    "delivery_report_url": delivery_report_url,
                    "keywords": keywords,
                    "service_code": service_code,
                    "target_system": target_system,
                },
                subscription_update_params.SubscriptionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionResponse,
        )

    async def delete(
        self,
        subscription_id: str,
        *,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubscriptionDeleteResponse:
        """
        This interface will stop our systems from sending Mobile originating messages
        and Delivery status reports to the provided delivery report and callback urls
        for a configured serviceCode.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subscription_id:
            raise ValueError(f"Expected a non-empty value for `subscription_id` but received {subscription_id!r}")
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return await self._delete(
            f"/messages/sms/subscription/{subscription_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubscriptionDeleteResponse,
        )


class SubscriptionResourceWithRawResponse:
    def __init__(self, subscription: SubscriptionResource) -> None:
        self._subscription = subscription

        self.create = to_raw_response_wrapper(
            subscription.create,
        )
        self.update = to_raw_response_wrapper(
            subscription.update,
        )
        self.delete = to_raw_response_wrapper(
            subscription.delete,
        )


class AsyncSubscriptionResourceWithRawResponse:
    def __init__(self, subscription: AsyncSubscriptionResource) -> None:
        self._subscription = subscription

        self.create = async_to_raw_response_wrapper(
            subscription.create,
        )
        self.update = async_to_raw_response_wrapper(
            subscription.update,
        )
        self.delete = async_to_raw_response_wrapper(
            subscription.delete,
        )


class SubscriptionResourceWithStreamingResponse:
    def __init__(self, subscription: SubscriptionResource) -> None:
        self._subscription = subscription

        self.create = to_streamed_response_wrapper(
            subscription.create,
        )
        self.update = to_streamed_response_wrapper(
            subscription.update,
        )
        self.delete = to_streamed_response_wrapper(
            subscription.delete,
        )


class AsyncSubscriptionResourceWithStreamingResponse:
    def __init__(self, subscription: AsyncSubscriptionResource) -> None:
        self._subscription = subscription

        self.create = async_to_streamed_response_wrapper(
            subscription.create,
        )
        self.update = async_to_streamed_response_wrapper(
            subscription.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            subscription.delete,
        )
