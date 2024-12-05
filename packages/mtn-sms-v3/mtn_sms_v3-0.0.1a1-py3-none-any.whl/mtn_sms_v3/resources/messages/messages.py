# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .sms import (
    SMSResource,
    AsyncSMSResource,
    SMSResourceWithRawResponse,
    AsyncSMSResourceWithRawResponse,
    SMSResourceWithStreamingResponse,
    AsyncSMSResourceWithStreamingResponse,
)
from .sms.sms import SMSResource, AsyncSMSResource
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["MessagesResource", "AsyncMessagesResource"]


class MessagesResource(SyncAPIResource):
    @cached_property
    def sms(self) -> SMSResource:
        return SMSResource(self._client)

    @cached_property
    def with_raw_response(self) -> MessagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#accessing-raw-response-data-eg-headers
        """
        return MessagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MessagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#with_streaming_response
        """
        return MessagesResourceWithStreamingResponse(self)


class AsyncMessagesResource(AsyncAPIResource):
    @cached_property
    def sms(self) -> AsyncSMSResource:
        return AsyncSMSResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMessagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#accessing-raw-response-data-eg-headers
        """
        return AsyncMessagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMessagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-sms-v3#with_streaming_response
        """
        return AsyncMessagesResourceWithStreamingResponse(self)


class MessagesResourceWithRawResponse:
    def __init__(self, messages: MessagesResource) -> None:
        self._messages = messages

    @cached_property
    def sms(self) -> SMSResourceWithRawResponse:
        return SMSResourceWithRawResponse(self._messages.sms)


class AsyncMessagesResourceWithRawResponse:
    def __init__(self, messages: AsyncMessagesResource) -> None:
        self._messages = messages

    @cached_property
    def sms(self) -> AsyncSMSResourceWithRawResponse:
        return AsyncSMSResourceWithRawResponse(self._messages.sms)


class MessagesResourceWithStreamingResponse:
    def __init__(self, messages: MessagesResource) -> None:
        self._messages = messages

    @cached_property
    def sms(self) -> SMSResourceWithStreamingResponse:
        return SMSResourceWithStreamingResponse(self._messages.sms)


class AsyncMessagesResourceWithStreamingResponse:
    def __init__(self, messages: AsyncMessagesResource) -> None:
        self._messages = messages

    @cached_property
    def sms(self) -> AsyncSMSResourceWithStreamingResponse:
        return AsyncSMSResourceWithStreamingResponse(self._messages.sms)
