# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from mtn_payments_v1 import MtnPaymentsV1, AsyncMtnPaymentsV1
from mtn_payments_v1._utils import parse_datetime
from mtn_payments_v1.types.payments import (
    PromiseToPayResponse,
    PromiseToPayEligibilityResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPaymentAgreement:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: MtnPaymentsV1) -> None:
        payment_agreement = client.payments.payment_agreement.create()
        assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: MtnPaymentsV1) -> None:
        payment_agreement = client.payments.payment_agreement.create(
            billing_account_no="903442299RC",
            duration_uom="Month",
            number_of_installments="3",
            promise_amount=1290,
            promise_open_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            promise_threshold="100",
            service_name="Outstanding Dues",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
        )
        assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: MtnPaymentsV1) -> None:
        response = client.payments.payment_agreement.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_agreement = response.parse()
        assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: MtnPaymentsV1) -> None:
        with client.payments.payment_agreement.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_agreement = response.parse()
            assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_eligibility(self, client: MtnPaymentsV1) -> None:
        payment_agreement = client.payments.payment_agreement.eligibility(
            billing_account_number="billingAccountNumber",
        )
        assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

    @parametrize
    def test_method_eligibility_with_all_params(self, client: MtnPaymentsV1) -> None:
        payment_agreement = client.payments.payment_agreement.eligibility(
            billing_account_number="billingAccountNumber",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
        )
        assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

    @parametrize
    def test_raw_response_eligibility(self, client: MtnPaymentsV1) -> None:
        response = client.payments.payment_agreement.with_raw_response.eligibility(
            billing_account_number="billingAccountNumber",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_agreement = response.parse()
        assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

    @parametrize
    def test_streaming_response_eligibility(self, client: MtnPaymentsV1) -> None:
        with client.payments.payment_agreement.with_streaming_response.eligibility(
            billing_account_number="billingAccountNumber",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_agreement = response.parse()
            assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPaymentAgreement:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment_agreement = await async_client.payments.payment_agreement.create()
        assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment_agreement = await async_client.payments.payment_agreement.create(
            billing_account_no="903442299RC",
            duration_uom="Month",
            number_of_installments="3",
            promise_amount=1290,
            promise_open_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            promise_threshold="100",
            service_name="Outstanding Dues",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
        )
        assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.payments.payment_agreement.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_agreement = await response.parse()
        assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.payments.payment_agreement.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_agreement = await response.parse()
            assert_matches_type(PromiseToPayResponse, payment_agreement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_eligibility(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment_agreement = await async_client.payments.payment_agreement.eligibility(
            billing_account_number="billingAccountNumber",
        )
        assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

    @parametrize
    async def test_method_eligibility_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment_agreement = await async_client.payments.payment_agreement.eligibility(
            billing_account_number="billingAccountNumber",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
        )
        assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

    @parametrize
    async def test_raw_response_eligibility(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.payments.payment_agreement.with_raw_response.eligibility(
            billing_account_number="billingAccountNumber",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment_agreement = await response.parse()
        assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

    @parametrize
    async def test_streaming_response_eligibility(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.payments.payment_agreement.with_streaming_response.eligibility(
            billing_account_number="billingAccountNumber",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment_agreement = await response.parse()
            assert_matches_type(PromiseToPayEligibilityResponse, payment_agreement, path=["response"])

        assert cast(Any, response.is_closed) is True
