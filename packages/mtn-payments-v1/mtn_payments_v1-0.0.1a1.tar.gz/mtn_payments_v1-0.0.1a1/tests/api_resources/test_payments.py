# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from mtn_payments_v1 import MtnPaymentsV1, AsyncMtnPaymentsV1
from mtn_payments_v1.types import (
    OrderResponse,
    InboundResponse,
    PaymentResponse,
    PaymentTransactionStatusResponse,
)
from mtn_payments_v1._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPayments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
        )
        assert_matches_type(PaymentResponse, payment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={
                "type": "BankCard",
                "description": "Manual Boost for RWC",
                "details": {
                    "account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "bank_account_debit": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_account_transfer": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_card": {
                        "bank": "Bank of Gotham",
                        "brand": "Visa",
                        "card_number": "xxxx xxxx xxx xxx",
                        "cvv": "123",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "last_four_digits": "1234",
                        "name_on_card": "Bruce Wayne",
                        "pin": "123",
                        "type": "Credit",
                    },
                    "bucket": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "digital_wallet": {
                        "service": "MoMo",
                        "wallet_id": "233364654737",
                        "wallet_uri": "https://paypal.me/johndoe",
                    },
                    "invoice": {
                        "id": "86rer4478878t991",
                        "callback_url": "https://merchant-application-url/webhook-endpoint",
                        "deactivate_on_fail": "true",
                        "end_date": "endDate",
                        "frequency": "on_call",
                        "retry_frequency": "once",
                        "retry_on_fail": True,
                        "retry_run": "1-5",
                        "start_date": "startDate",
                        "type": "trigger",
                    },
                    "loyalty_account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "tokenized_card": {
                        "token": "token",
                        "brand": "brand",
                        "issuer": "issuer",
                        "last_four_digits": "lastFourDigits",
                        "token_type": "tokenType",
                        "type": "type",
                    },
                    "voucher": {
                        "campaign": "campaign",
                        "code": "code",
                        "description": "description",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "value": "value",
                    },
                },
                "name": "Manual Boost for RWC",
                "valid_from": parse_datetime("2019-12-27T18:11:19.117Z"),
                "valid_to": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
            additional_information=[
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
            ],
            amount={
                "amount": 50,
                "units": "XOF",
            },
            authorization_code="authorizationCode",
            calling_system="ECW",
            channel="AYO",
            description="Manual Boost for RW",
            fee_bearer="Payer",
            name="Manual Boost for RWC",
            payee=[
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
            ],
            payer={
                "payer_id": "233364654737",
                "include_payer_charges": False,
                "payer_email": "payerEmail",
                "payer_id_type": "MSISDN",
                "payer_name": "payerName",
                "payer_note": "Manual Boost for RWC",
                "payer_ref": "233364654737",
                "payer_surname": "Orimoloye",
            },
            payment_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            quote_id="9223372036854775807",
            segment="subscriber",
            status="Pending",
            status_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            target_system="ECW",
            tax_amount={
                "amount": 50,
                "units": "XOF",
            },
            x_authorization="X-Authorization",
        )
        assert_matches_type(PaymentResponse, payment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: MtnPaymentsV1) -> None:
        response = client.payments.with_raw_response.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(PaymentResponse, payment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: MtnPaymentsV1) -> None:
        with client.payments.with_streaming_response.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(PaymentResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_fee(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
        )
        assert_matches_type(InboundResponse, payment, path=["response"])

    @parametrize
    def test_method_fee_with_all_params(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={
                "type": "BankCard",
                "description": "Manual Boost for RWC",
                "details": {
                    "account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "bank_account_debit": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_account_transfer": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_card": {
                        "bank": "Bank of Gotham",
                        "brand": "Visa",
                        "card_number": "xxxx xxxx xxx xxx",
                        "cvv": "123",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "last_four_digits": "1234",
                        "name_on_card": "Bruce Wayne",
                        "pin": "123",
                        "type": "Credit",
                    },
                    "bucket": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "digital_wallet": {
                        "service": "MoMo",
                        "wallet_id": "233364654737",
                        "wallet_uri": "https://paypal.me/johndoe",
                    },
                    "invoice": {
                        "id": "86rer4478878t991",
                        "callback_url": "https://merchant-application-url/webhook-endpoint",
                        "deactivate_on_fail": "true",
                        "end_date": "endDate",
                        "frequency": "on_call",
                        "retry_frequency": "once",
                        "retry_on_fail": True,
                        "retry_run": "1-5",
                        "start_date": "startDate",
                        "type": "trigger",
                    },
                    "loyalty_account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "tokenized_card": {
                        "token": "token",
                        "brand": "brand",
                        "issuer": "issuer",
                        "last_four_digits": "lastFourDigits",
                        "token_type": "tokenType",
                        "type": "type",
                    },
                    "voucher": {
                        "campaign": "campaign",
                        "code": "code",
                        "description": "description",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "value": "value",
                    },
                },
                "name": "Manual Boost for RWC",
                "valid_from": parse_datetime("2019-12-27T18:11:19.117Z"),
                "valid_to": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
            additional_information=[
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
            ],
            amount={
                "amount": 50,
                "units": "SWZ",
            },
            authorization_code="authorizationCode",
            calling_system="AYOBA",
            channel="AIRTIME",
            description="Manual Boost for RW",
            fee_bearer="Payer",
            name="Manual Boost for RWC",
            payee=[
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
            ],
            payer={
                "payer_id": "233364654737",
                "include_payer_charges": False,
                "payer_email": "payerEmail",
                "payer_id_type": "MSISDN",
                "payer_name": "payerName",
                "payer_note": "Manual Boost for RWC",
                "payer_ref": "233364654737",
                "payer_surname": "Orimoloye",
            },
            payment_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            quote_id="9223372036854775807",
            segment="subscriber",
            status="Pending",
            status_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            target_system="ECW",
            tax_amount={
                "amount": 50,
                "units": "SWZ",
            },
        )
        assert_matches_type(InboundResponse, payment, path=["response"])

    @parametrize
    def test_raw_response_fee(self, client: MtnPaymentsV1) -> None:
        response = client.payments.with_raw_response.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(InboundResponse, payment, path=["response"])

    @parametrize
    def test_streaming_response_fee(self, client: MtnPaymentsV1) -> None:
        with client.payments.with_streaming_response.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(InboundResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_payment_link(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.payment_link(
            body={},
        )
        assert_matches_type(OrderResponse, payment, path=["response"])

    @parametrize
    def test_method_payment_link_with_all_params(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.payment_link(
            body={},
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
        )
        assert_matches_type(OrderResponse, payment, path=["response"])

    @parametrize
    def test_raw_response_payment_link(self, client: MtnPaymentsV1) -> None:
        response = client.payments.with_raw_response.payment_link(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(OrderResponse, payment, path=["response"])

    @parametrize
    def test_streaming_response_payment_link(self, client: MtnPaymentsV1) -> None:
        with client.payments.with_streaming_response.payment_link(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(OrderResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_transaction_status(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
        )
        assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

    @parametrize
    def test_method_transaction_status_with_all_params(self, client: MtnPaymentsV1) -> None:
        payment = client.payments.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            amount=0,
            customer_id="customerId",
            description="description",
            payment_type="Airtime",
            target_system="EWP",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
            x_authorization="X-Authorization",
        )
        assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

    @parametrize
    def test_raw_response_transaction_status(self, client: MtnPaymentsV1) -> None:
        response = client.payments.with_raw_response.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

    @parametrize
    def test_streaming_response_transaction_status(self, client: MtnPaymentsV1) -> None:
        with client.payments.with_streaming_response.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_transaction_status(self, client: MtnPaymentsV1) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `correlator_id` but received ''"):
            client.payments.with_raw_response.transaction_status(
                correlator_id="",
            )


class TestAsyncPayments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
        )
        assert_matches_type(PaymentResponse, payment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={
                "type": "BankCard",
                "description": "Manual Boost for RWC",
                "details": {
                    "account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "bank_account_debit": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_account_transfer": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_card": {
                        "bank": "Bank of Gotham",
                        "brand": "Visa",
                        "card_number": "xxxx xxxx xxx xxx",
                        "cvv": "123",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "last_four_digits": "1234",
                        "name_on_card": "Bruce Wayne",
                        "pin": "123",
                        "type": "Credit",
                    },
                    "bucket": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "digital_wallet": {
                        "service": "MoMo",
                        "wallet_id": "233364654737",
                        "wallet_uri": "https://paypal.me/johndoe",
                    },
                    "invoice": {
                        "id": "86rer4478878t991",
                        "callback_url": "https://merchant-application-url/webhook-endpoint",
                        "deactivate_on_fail": "true",
                        "end_date": "endDate",
                        "frequency": "on_call",
                        "retry_frequency": "once",
                        "retry_on_fail": True,
                        "retry_run": "1-5",
                        "start_date": "startDate",
                        "type": "trigger",
                    },
                    "loyalty_account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "tokenized_card": {
                        "token": "token",
                        "brand": "brand",
                        "issuer": "issuer",
                        "last_four_digits": "lastFourDigits",
                        "token_type": "tokenType",
                        "type": "type",
                    },
                    "voucher": {
                        "campaign": "campaign",
                        "code": "code",
                        "description": "description",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "value": "value",
                    },
                },
                "name": "Manual Boost for RWC",
                "valid_from": parse_datetime("2019-12-27T18:11:19.117Z"),
                "valid_to": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
            additional_information=[
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
            ],
            amount={
                "amount": 50,
                "units": "XOF",
            },
            authorization_code="authorizationCode",
            calling_system="ECW",
            channel="AYO",
            description="Manual Boost for RW",
            fee_bearer="Payer",
            name="Manual Boost for RWC",
            payee=[
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
            ],
            payer={
                "payer_id": "233364654737",
                "include_payer_charges": False,
                "payer_email": "payerEmail",
                "payer_id_type": "MSISDN",
                "payer_name": "payerName",
                "payer_note": "Manual Boost for RWC",
                "payer_ref": "233364654737",
                "payer_surname": "Orimoloye",
            },
            payment_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            quote_id="9223372036854775807",
            segment="subscriber",
            status="Pending",
            status_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            target_system="ECW",
            tax_amount={
                "amount": 50,
                "units": "XOF",
            },
            x_authorization="X-Authorization",
        )
        assert_matches_type(PaymentResponse, payment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.payments.with_raw_response.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(PaymentResponse, payment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.payments.with_streaming_response.create(
            callback_url="https://myCallBack/url",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "XOF",
            },
            transaction_type="Payment",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(PaymentResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_fee(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
        )
        assert_matches_type(InboundResponse, payment, path=["response"])

    @parametrize
    async def test_method_fee_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={
                "type": "BankCard",
                "description": "Manual Boost for RWC",
                "details": {
                    "account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "bank_account_debit": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_account_transfer": {
                        "account_number": "accountNumber",
                        "account_number_type": "accountNumberType",
                        "bank": "bank",
                        "bic": "BIC",
                        "owner": "owner",
                    },
                    "bank_card": {
                        "bank": "Bank of Gotham",
                        "brand": "Visa",
                        "card_number": "xxxx xxxx xxx xxx",
                        "cvv": "123",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "last_four_digits": "1234",
                        "name_on_card": "Bruce Wayne",
                        "pin": "123",
                        "type": "Credit",
                    },
                    "bucket": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "digital_wallet": {
                        "service": "MoMo",
                        "wallet_id": "233364654737",
                        "wallet_uri": "https://paypal.me/johndoe",
                    },
                    "invoice": {
                        "id": "86rer4478878t991",
                        "callback_url": "https://merchant-application-url/webhook-endpoint",
                        "deactivate_on_fail": "true",
                        "end_date": "endDate",
                        "frequency": "on_call",
                        "retry_frequency": "once",
                        "retry_on_fail": True,
                        "retry_run": "1-5",
                        "start_date": "startDate",
                        "type": "trigger",
                    },
                    "loyalty_account": {
                        "id": "id",
                        "description": "description",
                        "name": "name",
                    },
                    "tokenized_card": {
                        "token": "token",
                        "brand": "brand",
                        "issuer": "issuer",
                        "last_four_digits": "lastFourDigits",
                        "token_type": "tokenType",
                        "type": "type",
                    },
                    "voucher": {
                        "campaign": "campaign",
                        "code": "code",
                        "description": "description",
                        "expiration_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "value": "value",
                    },
                },
                "name": "Manual Boost for RWC",
                "valid_from": parse_datetime("2019-12-27T18:11:19.117Z"),
                "valid_to": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
            additional_information=[
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
                {
                    "description": "Voice_1111",
                    "name": "BundleName",
                },
            ],
            amount={
                "amount": 50,
                "units": "SWZ",
            },
            authorization_code="authorizationCode",
            calling_system="AYOBA",
            channel="AIRTIME",
            description="Manual Boost for RW",
            fee_bearer="Payer",
            name="Manual Boost for RWC",
            payee=[
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
                {
                    "total_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                    "payee_id": "AYO.DEPOSIT",
                    "payee_id_type": "USER",
                    "payee_name": "payeeName",
                    "payee_note": "Manual Boost for RWC",
                    "tax_amount": {
                        "amount": 50,
                        "units": "XOF",
                    },
                },
            ],
            payer={
                "payer_id": "233364654737",
                "include_payer_charges": False,
                "payer_email": "payerEmail",
                "payer_id_type": "MSISDN",
                "payer_name": "payerName",
                "payer_note": "Manual Boost for RWC",
                "payer_ref": "233364654737",
                "payer_surname": "Orimoloye",
            },
            payment_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            quote_id="9223372036854775807",
            segment="subscriber",
            status="Pending",
            status_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            target_system="ECW",
            tax_amount={
                "amount": 50,
                "units": "SWZ",
            },
        )
        assert_matches_type(InboundResponse, payment, path=["response"])

    @parametrize
    async def test_raw_response_fee(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.payments.with_raw_response.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(InboundResponse, payment, path=["response"])

    @parametrize
    async def test_streaming_response_fee(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.payments.with_streaming_response.fee(
            callback_url="https://api.mtn.com/v1/callback",
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            payment_method={"type": "BankCard"},
            total_amount={
                "amount": 50,
                "units": "SWZ",
            },
            transaction_type="FeeCheck",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(InboundResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_payment_link(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.payment_link(
            body={},
        )
        assert_matches_type(OrderResponse, payment, path=["response"])

    @parametrize
    async def test_method_payment_link_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.payment_link(
            body={},
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
        )
        assert_matches_type(OrderResponse, payment, path=["response"])

    @parametrize
    async def test_raw_response_payment_link(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.payments.with_raw_response.payment_link(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(OrderResponse, payment, path=["response"])

    @parametrize
    async def test_streaming_response_payment_link(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.payments.with_streaming_response.payment_link(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(OrderResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_transaction_status(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
        )
        assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

    @parametrize
    async def test_method_transaction_status_with_all_params(self, async_client: AsyncMtnPaymentsV1) -> None:
        payment = await async_client.payments.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
            amount=0,
            customer_id="customerId",
            description="description",
            payment_type="Airtime",
            target_system="EWP",
            transaction_id="6f0bece6-7df3-4da4-af02-5e7f16e5e6fc",
            x_authorization="X-Authorization",
        )
        assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

    @parametrize
    async def test_raw_response_transaction_status(self, async_client: AsyncMtnPaymentsV1) -> None:
        response = await async_client.payments.with_raw_response.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

    @parametrize
    async def test_streaming_response_transaction_status(self, async_client: AsyncMtnPaymentsV1) -> None:
        async with async_client.payments.with_streaming_response.transaction_status(
            correlator_id="c5f80cb8-dc8b-11ea-87d0-0242ac130003",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(PaymentTransactionStatusResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_transaction_status(self, async_client: AsyncMtnPaymentsV1) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `correlator_id` but received ''"):
            await async_client.payments.with_raw_response.transaction_status(
                correlator_id="",
            )
