# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mtn_sms_v3 import MtnSMSV3, AsyncMtnSMSV3
from tests.utils import assert_matches_type
from mtn_sms_v3.types.messages.sms import (
    SubscriptionResponse,
    SubscriptionDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubscription:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: MtnSMSV3) -> None:
        subscription = client.messages.sms.subscription.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: MtnSMSV3) -> None:
        subscription = client.messages.sms.subscription.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
            delivery_report_url="https://example.com/delivery-report",
            transaction_id="transactionId",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: MtnSMSV3) -> None:
        response = client.messages.sms.subscription.with_raw_response.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: MtnSMSV3) -> None:
        with client.messages.sms.subscription.with_streaming_response.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: MtnSMSV3) -> None:
        subscription = client.messages.sms.subscription.update(
            subscription_id="subscriptionId",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: MtnSMSV3) -> None:
        subscription = client.messages.sms.subscription.update(
            subscription_id="subscriptionId",
            callback_url="http://www....",
            delivery_report_url="http://www....",
            keywords=["string", "string", "string"],
            service_code="serviceCode",
            target_system="targetSystem",
            transaction_id="transactionId",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: MtnSMSV3) -> None:
        response = client.messages.sms.subscription.with_raw_response.update(
            subscription_id="subscriptionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: MtnSMSV3) -> None:
        with client.messages.sms.subscription.with_streaming_response.update(
            subscription_id="subscriptionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: MtnSMSV3) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            client.messages.sms.subscription.with_raw_response.update(
                subscription_id="",
            )

    @parametrize
    def test_method_delete(self, client: MtnSMSV3) -> None:
        subscription = client.messages.sms.subscription.delete(
            subscription_id="27831234552920202220",
        )
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: MtnSMSV3) -> None:
        subscription = client.messages.sms.subscription.delete(
            subscription_id="27831234552920202220",
            transaction_id="transactionId",
        )
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: MtnSMSV3) -> None:
        response = client.messages.sms.subscription.with_raw_response.delete(
            subscription_id="27831234552920202220",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: MtnSMSV3) -> None:
        with client.messages.sms.subscription.with_streaming_response.delete(
            subscription_id="27831234552920202220",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: MtnSMSV3) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            client.messages.sms.subscription.with_raw_response.delete(
                subscription_id="",
            )


class TestAsyncSubscription:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMtnSMSV3) -> None:
        subscription = await async_client.messages.sms.subscription.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMtnSMSV3) -> None:
        subscription = await async_client.messages.sms.subscription.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
            delivery_report_url="https://example.com/delivery-report",
            transaction_id="transactionId",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMtnSMSV3) -> None:
        response = await async_client.messages.sms.subscription.with_raw_response.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMtnSMSV3) -> None:
        async with async_client.messages.sms.subscription.with_streaming_response.create(
            callback_url="https://example.com/12acb41",
            service_code="serviceCode",
            target_system="Golden-Bank",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncMtnSMSV3) -> None:
        subscription = await async_client.messages.sms.subscription.update(
            subscription_id="subscriptionId",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncMtnSMSV3) -> None:
        subscription = await async_client.messages.sms.subscription.update(
            subscription_id="subscriptionId",
            callback_url="http://www....",
            delivery_report_url="http://www....",
            keywords=["string", "string", "string"],
            service_code="serviceCode",
            target_system="targetSystem",
            transaction_id="transactionId",
        )
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncMtnSMSV3) -> None:
        response = await async_client.messages.sms.subscription.with_raw_response.update(
            subscription_id="subscriptionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionResponse, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncMtnSMSV3) -> None:
        async with async_client.messages.sms.subscription.with_streaming_response.update(
            subscription_id="subscriptionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncMtnSMSV3) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            await async_client.messages.sms.subscription.with_raw_response.update(
                subscription_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncMtnSMSV3) -> None:
        subscription = await async_client.messages.sms.subscription.delete(
            subscription_id="27831234552920202220",
        )
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncMtnSMSV3) -> None:
        subscription = await async_client.messages.sms.subscription.delete(
            subscription_id="27831234552920202220",
            transaction_id="transactionId",
        )
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncMtnSMSV3) -> None:
        response = await async_client.messages.sms.subscription.with_raw_response.delete(
            subscription_id="27831234552920202220",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncMtnSMSV3) -> None:
        async with async_client.messages.sms.subscription.with_streaming_response.delete(
            subscription_id="27831234552920202220",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncMtnSMSV3) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subscription_id` but received ''"):
            await async_client.messages.sms.subscription.with_raw_response.delete(
                subscription_id="",
            )
