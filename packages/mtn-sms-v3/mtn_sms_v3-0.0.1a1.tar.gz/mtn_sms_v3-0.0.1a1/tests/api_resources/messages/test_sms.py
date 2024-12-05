# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mtn_sms_v3 import MtnSMSV3, AsyncMtnSMSV3
from tests.utils import assert_matches_type
from mtn_sms_v3.types.messages import ResourceReference

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSMS:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_outbound(self, client: MtnSMSV3) -> None:
        sms = client.messages.sms.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
        )
        assert_matches_type(ResourceReference, sms, path=["response"])

    @parametrize
    def test_method_outbound_with_all_params(self, client: MtnSMSV3) -> None:
        sms = client.messages.sms.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
            keyword="keyword",
            request_delivery_receipt=False,
            sender_address="MTN",
        )
        assert_matches_type(ResourceReference, sms, path=["response"])

    @parametrize
    def test_raw_response_outbound(self, client: MtnSMSV3) -> None:
        response = client.messages.sms.with_raw_response.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sms = response.parse()
        assert_matches_type(ResourceReference, sms, path=["response"])

    @parametrize
    def test_streaming_response_outbound(self, client: MtnSMSV3) -> None:
        with client.messages.sms.with_streaming_response.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sms = response.parse()
            assert_matches_type(ResourceReference, sms, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSMS:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_outbound(self, async_client: AsyncMtnSMSV3) -> None:
        sms = await async_client.messages.sms.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
        )
        assert_matches_type(ResourceReference, sms, path=["response"])

    @parametrize
    async def test_method_outbound_with_all_params(self, async_client: AsyncMtnSMSV3) -> None:
        sms = await async_client.messages.sms.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
            keyword="keyword",
            request_delivery_receipt=False,
            sender_address="MTN",
        )
        assert_matches_type(ResourceReference, sms, path=["response"])

    @parametrize
    async def test_raw_response_outbound(self, async_client: AsyncMtnSMSV3) -> None:
        response = await async_client.messages.sms.with_raw_response.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sms = await response.parse()
        assert_matches_type(ResourceReference, sms, path=["response"])

    @parametrize
    async def test_streaming_response_outbound(self, async_client: AsyncMtnSMSV3) -> None:
        async with async_client.messages.sms.with_streaming_response.outbound(
            client_correlator_id="clientCorrelatorId",
            message="message",
            receiver_address=["23423456789", "23423456790"],
            service_code="11221 or 131",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sms = await response.parse()
            assert_matches_type(ResourceReference, sms, path=["response"])

        assert cast(Any, response.is_closed) is True
