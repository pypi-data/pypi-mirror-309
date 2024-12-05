# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from mtn_payments_v1 import MtnPaymentsV1, AsyncMtnPaymentsV1
from mtn_payments_v1.types import ReverseTransactionHistory

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReversePayments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_history(self, client: MtnPaymentsV1) -> None:
        reverse_payment = client.reverse_payments.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
        )
        assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

    @parametrize
    def test_method_history_with_all_params(self, client: MtnPaymentsV1) -> None:
        reverse_payment = client.reverse_payments.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
            amount=0,
            end_date="endDate",
            limit=0,
            node_id="nodeId",
            other_fri="otherFri",
            page_no=0,
            pos_msisdn="posMsisdn",
            quote_id="quoteId",
            start_date="startDate",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
            transactionstatus="transactionstatus",
            x_authorization="X-Authorization",
        )
        assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

    @parametrize
    def test_raw_response_history(self, client: MtnPaymentsV1) -> None:
        response = client.reverse_payments.with_raw_response.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        reverse_payment = response.parse()
        assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

    @parametrize
    def test_streaming_response_history(self, client: MtnPaymentsV1) -> None:
        with client.reverse_payments.with_streaming_response.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            reverse_payment = response.parse()
            assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncReversePayments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_history(self, async_client: AsyncMtnPaymentsV1) -> None:
        reverse_payment = await async_client.reverse_payments.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
        )
        assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

    @parametrize
    async def test_method_history_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        reverse_payment = await async_client.reverse_payments.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
            amount=0,
            end_date="endDate",
            limit=0,
            node_id="nodeId",
            other_fri="otherFri",
            page_no=0,
            pos_msisdn="posMsisdn",
            quote_id="quoteId",
            start_date="startDate",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
            transactionstatus="transactionstatus",
            x_authorization="X-Authorization",
        )
        assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

    @parametrize
    async def test_raw_response_history(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.reverse_payments.with_raw_response.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        reverse_payment = await response.parse()
        assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

    @parametrize
    async def test_streaming_response_history(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.reverse_payments.with_streaming_response.history(
            transactiontype="transactiontype",
            customer_id="FRI:266456789/MSISDN",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            reverse_payment = await response.parse()
            assert_matches_type(ReverseTransactionHistory, reverse_payment, path=["response"])

        assert cast(Any, response.is_closed) is True
