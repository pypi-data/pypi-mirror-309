# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from datetime import datetime
from typing_extensions import Literal

import httpx

from ...types import (
    payment_fee_params,
    payment_create_params,
    payment_payment_link_params,
    payment_transaction_status_params,
)
from .history import (
    HistoryResource,
    AsyncHistoryResource,
    HistoryResourceWithRawResponse,
    AsyncHistoryResourceWithRawResponse,
    HistoryResourceWithStreamingResponse,
    AsyncHistoryResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .payment_agreement import (
    PaymentAgreementResource,
    AsyncPaymentAgreementResource,
    PaymentAgreementResourceWithRawResponse,
    AsyncPaymentAgreementResourceWithRawResponse,
    PaymentAgreementResourceWithStreamingResponse,
    AsyncPaymentAgreementResourceWithStreamingResponse,
)
from ...types.order_response import OrderResponse
from ...types.inbound_response import InboundResponse
from ...types.payment_response import PaymentResponse
from ...types.payment_transaction_status_response import PaymentTransactionStatusResponse

__all__ = ["PaymentsResource", "AsyncPaymentsResource"]


class PaymentsResource(SyncAPIResource):
    @cached_property
    def history(self) -> HistoryResource:
        return HistoryResource(self._client)

    @cached_property
    def payment_agreement(self) -> PaymentAgreementResource:
        return PaymentAgreementResource(self._client)

    @cached_property
    def with_raw_response(self) -> PaymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return PaymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PaymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return PaymentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        callback_url: str,
        correlator_id: str,
        payment_method: payment_create_params.PaymentMethod,
        total_amount: payment_create_params.TotalAmount,
        transaction_type: Literal["Payment", "Debit", "Transfer", "Refund"],
        additional_information: Iterable[payment_create_params.AdditionalInformation] | NotGiven = NOT_GIVEN,
        amount: payment_create_params.Amount | NotGiven = NOT_GIVEN,
        authorization_code: str | NotGiven = NOT_GIVEN,
        calling_system: Literal["ECW", "AYO", "POS", "IVR"] | NotGiven = NOT_GIVEN,
        channel: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        fee_bearer: Literal["Payer", "Payee"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        payee: Iterable[payment_create_params.Payee] | NotGiven = NOT_GIVEN,
        payer: payment_create_params.Payer | NotGiven = NOT_GIVEN,
        payment_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        quote_id: str | NotGiven = NOT_GIVEN,
        segment: Literal["subscriber", "agent", "merchant", "admin"] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        status_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        target_system: Literal["ECW", "AYO", "EWP", "OCC", "CPG", "CELD"] | NotGiven = NOT_GIVEN,
        tax_amount: payment_create_params.TaxAmount | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentResponse:
        """
        Provides the ability for a consumer to make a payment or refund to service
        providers.

        Args:
          callback_url: The callback URL.

          correlator_id: Unique identifier in the client for the payment in case it is needed to
              correlate, a trace id associated with the caller

          payment_method: Reference or value of the method used to process the payment.

          total_amount: Representation of monetary value.

          transaction_type: The transaction type that is associated with the payment transaction.

          amount: Representation of monetary value.

          authorization_code: Authorization code retrieved from an external payment gateway that could be used
              for conciliation.

          calling_system: The name of the calling system.

          channel: The channel used to perform the payment operation or just the channel itself
              with just its name.

          description: Text describing the contents of the payment.

          fee_bearer: Who bears a charge for a particular transaction , whether a Payer or Payee

          name: Screen name of the payment.

          payer: The individual that performs the payment.

          payment_date: Date when the payment was performed.

          quote_id: The ID of the quote used, a terminal id associated with the caller.

          segment: Segment of the customer. Forexample, subscriber,agent, merchant, admin depending
              on the type of customer whome the operation is being performed against.

          status: Status of the payment method.

          status_date: Time the status of the payment method changed.

          target_system: The name of the target system.

          tax_amount: Representation of monetary value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"X-Authorization": x_authorization}), **(extra_headers or {})}
        return self._post(
            "/payments",
            body=maybe_transform(
                {
                    "callback_url": callback_url,
                    "correlator_id": correlator_id,
                    "payment_method": payment_method,
                    "total_amount": total_amount,
                    "transaction_type": transaction_type,
                    "additional_information": additional_information,
                    "amount": amount,
                    "authorization_code": authorization_code,
                    "calling_system": calling_system,
                    "channel": channel,
                    "description": description,
                    "fee_bearer": fee_bearer,
                    "name": name,
                    "payee": payee,
                    "payer": payer,
                    "payment_date": payment_date,
                    "quote_id": quote_id,
                    "segment": segment,
                    "status": status,
                    "status_date": status_date,
                    "target_system": target_system,
                    "tax_amount": tax_amount,
                },
                payment_create_params.PaymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PaymentResponse,
        )

    def fee(
        self,
        *,
        callback_url: str,
        correlator_id: str,
        payment_method: payment_fee_params.PaymentMethod,
        total_amount: payment_fee_params.TotalAmount,
        transaction_type: str,
        additional_information: Iterable[payment_fee_params.AdditionalInformation] | NotGiven = NOT_GIVEN,
        amount: payment_fee_params.Amount | NotGiven = NOT_GIVEN,
        authorization_code: str | NotGiven = NOT_GIVEN,
        calling_system: str | NotGiven = NOT_GIVEN,
        channel: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        fee_bearer: Literal["Payer", "Payee"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        payee: Iterable[payment_fee_params.Payee] | NotGiven = NOT_GIVEN,
        payer: payment_fee_params.Payer | NotGiven = NOT_GIVEN,
        payment_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        quote_id: str | NotGiven = NOT_GIVEN,
        segment: Literal["subscriber", "agent", "merchant", "admin"] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        status_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        target_system: str | NotGiven = NOT_GIVEN,
        tax_amount: payment_fee_params.TaxAmount | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> InboundResponse:
        """
        Provides the ability for a consumer to check a payment transfer fee charged by
        service providers.

        Args:
          callback_url: The callback URL.

          correlator_id: Unique identifier in the client for the payment in case it is needed to
              correlate, a trace id associated with the caller

          payment_method: Reference or value of the method used to process the payment.

          total_amount: Representation of SWZ monetary value.

          transaction_type: calling systemn.

          amount: Representation of SWZ monetary value.

          authorization_code: Authorization code retrieved from an external payment gateway that could be used
              for conciliation.

          calling_system: calling system.

          channel: The channel used to perform the payment operation or just the channel itself
              with just its name.

          description: Text describing the contents of the payment.

          fee_bearer: Who bears a charge for a particular transaction , whether a Payer or Payee

          name: Screen name of the payment.

          payer: The individual that performs the payment.

          payment_date: Date when the payment was performed.

          quote_id: The ID of the quote used, a terminal id associated with the caller.

          segment: Segment of the customer. Forexample, subscriber,agent, merchant, admin depending
              on the type of customer whome the operation is being performed against.

          status: Status of the payment method.

          status_date: Time the status of the payment method changed.

          target_system: calling systemn.

          tax_amount: Representation of SWZ monetary value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/payments/fee",
            body=maybe_transform(
                {
                    "callback_url": callback_url,
                    "correlator_id": correlator_id,
                    "payment_method": payment_method,
                    "total_amount": total_amount,
                    "transaction_type": transaction_type,
                    "additional_information": additional_information,
                    "amount": amount,
                    "authorization_code": authorization_code,
                    "calling_system": calling_system,
                    "channel": channel,
                    "description": description,
                    "fee_bearer": fee_bearer,
                    "name": name,
                    "payee": payee,
                    "payer": payer,
                    "payment_date": payment_date,
                    "quote_id": quote_id,
                    "segment": segment,
                    "status": status,
                    "status_date": status_date,
                    "target_system": target_system,
                    "tax_amount": tax_amount,
                },
                payment_fee_params.PaymentFeeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InboundResponse,
        )

    def payment_link(
        self,
        *,
        body: object,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderResponse:
        """
        Provides the ability for a consumer to get the payment link for the requesting
        MSISDN so as to enable the customer to make payment to the service providers.

        Args:
          body: Order Request details.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return self._post(
            "/payments/payment-link",
            body=maybe_transform(body, payment_payment_link_params.PaymentPaymentLinkParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderResponse,
        )

    def transaction_status(
        self,
        correlator_id: str,
        *,
        amount: float | NotGiven = NOT_GIVEN,
        customer_id: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        payment_type: Literal["Airtime"] | NotGiven = NOT_GIVEN,
        target_system: Literal["EWP", "ECW", "CELD"] | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentTransactionStatusResponse:
        """
        Provides the status of a Payment Transaction to service providers.

        Args:
          customer_id: This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN

          description: can be a payer note, a merchant identifier ie. merchantId etc.

          payment_type: Type of the transaction

          target_system: target system expected to fulful the service

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not correlator_id:
            raise ValueError(f"Expected a non-empty value for `correlator_id` but received {correlator_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "transactionId": transaction_id,
                    "X-Authorization": x_authorization,
                }
            ),
            **(extra_headers or {}),
        }
        return self._get(
            f"/payments/{correlator_id}/transactionStatus",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "amount": amount,
                        "customer_id": customer_id,
                        "description": description,
                        "payment_type": payment_type,
                        "target_system": target_system,
                    },
                    payment_transaction_status_params.PaymentTransactionStatusParams,
                ),
            ),
            cast_to=PaymentTransactionStatusResponse,
        )


class AsyncPaymentsResource(AsyncAPIResource):
    @cached_property
    def history(self) -> AsyncHistoryResource:
        return AsyncHistoryResource(self._client)

    @cached_property
    def payment_agreement(self) -> AsyncPaymentAgreementResource:
        return AsyncPaymentAgreementResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPaymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return AsyncPaymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPaymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return AsyncPaymentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        callback_url: str,
        correlator_id: str,
        payment_method: payment_create_params.PaymentMethod,
        total_amount: payment_create_params.TotalAmount,
        transaction_type: Literal["Payment", "Debit", "Transfer", "Refund"],
        additional_information: Iterable[payment_create_params.AdditionalInformation] | NotGiven = NOT_GIVEN,
        amount: payment_create_params.Amount | NotGiven = NOT_GIVEN,
        authorization_code: str | NotGiven = NOT_GIVEN,
        calling_system: Literal["ECW", "AYO", "POS", "IVR"] | NotGiven = NOT_GIVEN,
        channel: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        fee_bearer: Literal["Payer", "Payee"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        payee: Iterable[payment_create_params.Payee] | NotGiven = NOT_GIVEN,
        payer: payment_create_params.Payer | NotGiven = NOT_GIVEN,
        payment_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        quote_id: str | NotGiven = NOT_GIVEN,
        segment: Literal["subscriber", "agent", "merchant", "admin"] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        status_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        target_system: Literal["ECW", "AYO", "EWP", "OCC", "CPG", "CELD"] | NotGiven = NOT_GIVEN,
        tax_amount: payment_create_params.TaxAmount | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentResponse:
        """
        Provides the ability for a consumer to make a payment or refund to service
        providers.

        Args:
          callback_url: The callback URL.

          correlator_id: Unique identifier in the client for the payment in case it is needed to
              correlate, a trace id associated with the caller

          payment_method: Reference or value of the method used to process the payment.

          total_amount: Representation of monetary value.

          transaction_type: The transaction type that is associated with the payment transaction.

          amount: Representation of monetary value.

          authorization_code: Authorization code retrieved from an external payment gateway that could be used
              for conciliation.

          calling_system: The name of the calling system.

          channel: The channel used to perform the payment operation or just the channel itself
              with just its name.

          description: Text describing the contents of the payment.

          fee_bearer: Who bears a charge for a particular transaction , whether a Payer or Payee

          name: Screen name of the payment.

          payer: The individual that performs the payment.

          payment_date: Date when the payment was performed.

          quote_id: The ID of the quote used, a terminal id associated with the caller.

          segment: Segment of the customer. Forexample, subscriber,agent, merchant, admin depending
              on the type of customer whome the operation is being performed against.

          status: Status of the payment method.

          status_date: Time the status of the payment method changed.

          target_system: The name of the target system.

          tax_amount: Representation of monetary value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"X-Authorization": x_authorization}), **(extra_headers or {})}
        return await self._post(
            "/payments",
            body=await async_maybe_transform(
                {
                    "callback_url": callback_url,
                    "correlator_id": correlator_id,
                    "payment_method": payment_method,
                    "total_amount": total_amount,
                    "transaction_type": transaction_type,
                    "additional_information": additional_information,
                    "amount": amount,
                    "authorization_code": authorization_code,
                    "calling_system": calling_system,
                    "channel": channel,
                    "description": description,
                    "fee_bearer": fee_bearer,
                    "name": name,
                    "payee": payee,
                    "payer": payer,
                    "payment_date": payment_date,
                    "quote_id": quote_id,
                    "segment": segment,
                    "status": status,
                    "status_date": status_date,
                    "target_system": target_system,
                    "tax_amount": tax_amount,
                },
                payment_create_params.PaymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PaymentResponse,
        )

    async def fee(
        self,
        *,
        callback_url: str,
        correlator_id: str,
        payment_method: payment_fee_params.PaymentMethod,
        total_amount: payment_fee_params.TotalAmount,
        transaction_type: str,
        additional_information: Iterable[payment_fee_params.AdditionalInformation] | NotGiven = NOT_GIVEN,
        amount: payment_fee_params.Amount | NotGiven = NOT_GIVEN,
        authorization_code: str | NotGiven = NOT_GIVEN,
        calling_system: str | NotGiven = NOT_GIVEN,
        channel: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        fee_bearer: Literal["Payer", "Payee"] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        payee: Iterable[payment_fee_params.Payee] | NotGiven = NOT_GIVEN,
        payer: payment_fee_params.Payer | NotGiven = NOT_GIVEN,
        payment_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        quote_id: str | NotGiven = NOT_GIVEN,
        segment: Literal["subscriber", "agent", "merchant", "admin"] | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        status_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        target_system: str | NotGiven = NOT_GIVEN,
        tax_amount: payment_fee_params.TaxAmount | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> InboundResponse:
        """
        Provides the ability for a consumer to check a payment transfer fee charged by
        service providers.

        Args:
          callback_url: The callback URL.

          correlator_id: Unique identifier in the client for the payment in case it is needed to
              correlate, a trace id associated with the caller

          payment_method: Reference or value of the method used to process the payment.

          total_amount: Representation of SWZ monetary value.

          transaction_type: calling systemn.

          amount: Representation of SWZ monetary value.

          authorization_code: Authorization code retrieved from an external payment gateway that could be used
              for conciliation.

          calling_system: calling system.

          channel: The channel used to perform the payment operation or just the channel itself
              with just its name.

          description: Text describing the contents of the payment.

          fee_bearer: Who bears a charge for a particular transaction , whether a Payer or Payee

          name: Screen name of the payment.

          payer: The individual that performs the payment.

          payment_date: Date when the payment was performed.

          quote_id: The ID of the quote used, a terminal id associated with the caller.

          segment: Segment of the customer. Forexample, subscriber,agent, merchant, admin depending
              on the type of customer whome the operation is being performed against.

          status: Status of the payment method.

          status_date: Time the status of the payment method changed.

          target_system: calling systemn.

          tax_amount: Representation of SWZ monetary value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/payments/fee",
            body=await async_maybe_transform(
                {
                    "callback_url": callback_url,
                    "correlator_id": correlator_id,
                    "payment_method": payment_method,
                    "total_amount": total_amount,
                    "transaction_type": transaction_type,
                    "additional_information": additional_information,
                    "amount": amount,
                    "authorization_code": authorization_code,
                    "calling_system": calling_system,
                    "channel": channel,
                    "description": description,
                    "fee_bearer": fee_bearer,
                    "name": name,
                    "payee": payee,
                    "payer": payer,
                    "payment_date": payment_date,
                    "quote_id": quote_id,
                    "segment": segment,
                    "status": status,
                    "status_date": status_date,
                    "target_system": target_system,
                    "tax_amount": tax_amount,
                },
                payment_fee_params.PaymentFeeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InboundResponse,
        )

    async def payment_link(
        self,
        *,
        body: object,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderResponse:
        """
        Provides the ability for a consumer to get the payment link for the requesting
        MSISDN so as to enable the customer to make payment to the service providers.

        Args:
          body: Order Request details.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return await self._post(
            "/payments/payment-link",
            body=await async_maybe_transform(body, payment_payment_link_params.PaymentPaymentLinkParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderResponse,
        )

    async def transaction_status(
        self,
        correlator_id: str,
        *,
        amount: float | NotGiven = NOT_GIVEN,
        customer_id: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        payment_type: Literal["Airtime"] | NotGiven = NOT_GIVEN,
        target_system: Literal["EWP", "ECW", "CELD"] | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentTransactionStatusResponse:
        """
        Provides the status of a Payment Transaction to service providers.

        Args:
          customer_id: This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN

          description: can be a payer note, a merchant identifier ie. merchantId etc.

          payment_type: Type of the transaction

          target_system: target system expected to fulful the service

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not correlator_id:
            raise ValueError(f"Expected a non-empty value for `correlator_id` but received {correlator_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "transactionId": transaction_id,
                    "X-Authorization": x_authorization,
                }
            ),
            **(extra_headers or {}),
        }
        return await self._get(
            f"/payments/{correlator_id}/transactionStatus",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "amount": amount,
                        "customer_id": customer_id,
                        "description": description,
                        "payment_type": payment_type,
                        "target_system": target_system,
                    },
                    payment_transaction_status_params.PaymentTransactionStatusParams,
                ),
            ),
            cast_to=PaymentTransactionStatusResponse,
        )


class PaymentsResourceWithRawResponse:
    def __init__(self, payments: PaymentsResource) -> None:
        self._payments = payments

        self.create = to_raw_response_wrapper(
            payments.create,
        )
        self.fee = to_raw_response_wrapper(
            payments.fee,
        )
        self.payment_link = to_raw_response_wrapper(
            payments.payment_link,
        )
        self.transaction_status = to_raw_response_wrapper(
            payments.transaction_status,
        )

    @cached_property
    def history(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self._payments.history)

    @cached_property
    def payment_agreement(self) -> PaymentAgreementResourceWithRawResponse:
        return PaymentAgreementResourceWithRawResponse(self._payments.payment_agreement)


class AsyncPaymentsResourceWithRawResponse:
    def __init__(self, payments: AsyncPaymentsResource) -> None:
        self._payments = payments

        self.create = async_to_raw_response_wrapper(
            payments.create,
        )
        self.fee = async_to_raw_response_wrapper(
            payments.fee,
        )
        self.payment_link = async_to_raw_response_wrapper(
            payments.payment_link,
        )
        self.transaction_status = async_to_raw_response_wrapper(
            payments.transaction_status,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self._payments.history)

    @cached_property
    def payment_agreement(self) -> AsyncPaymentAgreementResourceWithRawResponse:
        return AsyncPaymentAgreementResourceWithRawResponse(self._payments.payment_agreement)


class PaymentsResourceWithStreamingResponse:
    def __init__(self, payments: PaymentsResource) -> None:
        self._payments = payments

        self.create = to_streamed_response_wrapper(
            payments.create,
        )
        self.fee = to_streamed_response_wrapper(
            payments.fee,
        )
        self.payment_link = to_streamed_response_wrapper(
            payments.payment_link,
        )
        self.transaction_status = to_streamed_response_wrapper(
            payments.transaction_status,
        )

    @cached_property
    def history(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self._payments.history)

    @cached_property
    def payment_agreement(self) -> PaymentAgreementResourceWithStreamingResponse:
        return PaymentAgreementResourceWithStreamingResponse(self._payments.payment_agreement)


class AsyncPaymentsResourceWithStreamingResponse:
    def __init__(self, payments: AsyncPaymentsResource) -> None:
        self._payments = payments

        self.create = async_to_streamed_response_wrapper(
            payments.create,
        )
        self.fee = async_to_streamed_response_wrapper(
            payments.fee,
        )
        self.payment_link = async_to_streamed_response_wrapper(
            payments.payment_link,
        )
        self.transaction_status = async_to_streamed_response_wrapper(
            payments.transaction_status,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self._payments.history)

    @cached_property
    def payment_agreement(self) -> AsyncPaymentAgreementResourceWithStreamingResponse:
        return AsyncPaymentAgreementResourceWithStreamingResponse(self._payments.payment_agreement)
