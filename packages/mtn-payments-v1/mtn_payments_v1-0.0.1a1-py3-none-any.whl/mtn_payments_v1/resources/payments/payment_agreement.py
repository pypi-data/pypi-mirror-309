# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime

import httpx

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
from ...types.payments import payment_agreement_create_params, payment_agreement_eligibility_params
from ...types.payments.promise_to_pay_response import PromiseToPayResponse
from ...types.payments.promise_to_pay_eligibility_response import PromiseToPayEligibilityResponse

__all__ = ["PaymentAgreementResource", "AsyncPaymentAgreementResource"]


class PaymentAgreementResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PaymentAgreementResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return PaymentAgreementResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PaymentAgreementResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return PaymentAgreementResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        billing_account_no: str | NotGiven = NOT_GIVEN,
        duration_uom: str | NotGiven = NOT_GIVEN,
        number_of_installments: str | NotGiven = NOT_GIVEN,
        promise_amount: float | NotGiven = NOT_GIVEN,
        promise_open_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        promise_threshold: str | NotGiven = NOT_GIVEN,
        service_name: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromiseToPayResponse:
        """
        Provides the ability for a consumer to generate a payment agreement (Promise to
        Pay) so as to enable the customer to make payment to the service providers.

        Args:
          billing_account_no: Unique Billing Account number of the customer

          duration_uom: Unit of Measure for the EMI (can be Month, Week and Year).

          number_of_installments: Number of the EMI.

          promise_amount: Amount promised to be paid.

          promise_open_date: Start Date of the Promise.

          promise_threshold: The Promise Threshold

          service_name: Service name of the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return self._post(
            "/payments/payment-agreement",
            body=maybe_transform(
                {
                    "billing_account_no": billing_account_no,
                    "duration_uom": duration_uom,
                    "number_of_installments": number_of_installments,
                    "promise_amount": promise_amount,
                    "promise_open_date": promise_open_date,
                    "promise_threshold": promise_threshold,
                    "service_name": service_name,
                },
                payment_agreement_create_params.PaymentAgreementCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromiseToPayResponse,
        )

    def eligibility(
        self,
        *,
        billing_account_number: str,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromiseToPayEligibilityResponse:
        """
        Provides the ability for a consumer to check the eligibility status for payment
        agreement so as to enable the customer to make payment to the service providers.

        Args:
          billing_account_number: Singleview billing account number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return self._get(
            "/payments/payment-agreement/eligibility",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"billing_account_number": billing_account_number},
                    payment_agreement_eligibility_params.PaymentAgreementEligibilityParams,
                ),
            ),
            cast_to=PromiseToPayEligibilityResponse,
        )


class AsyncPaymentAgreementResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPaymentAgreementResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return AsyncPaymentAgreementResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPaymentAgreementResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return AsyncPaymentAgreementResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        billing_account_no: str | NotGiven = NOT_GIVEN,
        duration_uom: str | NotGiven = NOT_GIVEN,
        number_of_installments: str | NotGiven = NOT_GIVEN,
        promise_amount: float | NotGiven = NOT_GIVEN,
        promise_open_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        promise_threshold: str | NotGiven = NOT_GIVEN,
        service_name: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromiseToPayResponse:
        """
        Provides the ability for a consumer to generate a payment agreement (Promise to
        Pay) so as to enable the customer to make payment to the service providers.

        Args:
          billing_account_no: Unique Billing Account number of the customer

          duration_uom: Unit of Measure for the EMI (can be Month, Week and Year).

          number_of_installments: Number of the EMI.

          promise_amount: Amount promised to be paid.

          promise_open_date: Start Date of the Promise.

          promise_threshold: The Promise Threshold

          service_name: Service name of the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return await self._post(
            "/payments/payment-agreement",
            body=await async_maybe_transform(
                {
                    "billing_account_no": billing_account_no,
                    "duration_uom": duration_uom,
                    "number_of_installments": number_of_installments,
                    "promise_amount": promise_amount,
                    "promise_open_date": promise_open_date,
                    "promise_threshold": promise_threshold,
                    "service_name": service_name,
                },
                payment_agreement_create_params.PaymentAgreementCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromiseToPayResponse,
        )

    async def eligibility(
        self,
        *,
        billing_account_number: str,
        transaction_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromiseToPayEligibilityResponse:
        """
        Provides the ability for a consumer to check the eligibility status for payment
        agreement so as to enable the customer to make payment to the service providers.

        Args:
          billing_account_number: Singleview billing account number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"transactionId": transaction_id}), **(extra_headers or {})}
        return await self._get(
            "/payments/payment-agreement/eligibility",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"billing_account_number": billing_account_number},
                    payment_agreement_eligibility_params.PaymentAgreementEligibilityParams,
                ),
            ),
            cast_to=PromiseToPayEligibilityResponse,
        )


class PaymentAgreementResourceWithRawResponse:
    def __init__(self, payment_agreement: PaymentAgreementResource) -> None:
        self._payment_agreement = payment_agreement

        self.create = to_raw_response_wrapper(
            payment_agreement.create,
        )
        self.eligibility = to_raw_response_wrapper(
            payment_agreement.eligibility,
        )


class AsyncPaymentAgreementResourceWithRawResponse:
    def __init__(self, payment_agreement: AsyncPaymentAgreementResource) -> None:
        self._payment_agreement = payment_agreement

        self.create = async_to_raw_response_wrapper(
            payment_agreement.create,
        )
        self.eligibility = async_to_raw_response_wrapper(
            payment_agreement.eligibility,
        )


class PaymentAgreementResourceWithStreamingResponse:
    def __init__(self, payment_agreement: PaymentAgreementResource) -> None:
        self._payment_agreement = payment_agreement

        self.create = to_streamed_response_wrapper(
            payment_agreement.create,
        )
        self.eligibility = to_streamed_response_wrapper(
            payment_agreement.eligibility,
        )


class AsyncPaymentAgreementResourceWithStreamingResponse:
    def __init__(self, payment_agreement: AsyncPaymentAgreementResource) -> None:
        self._payment_agreement = payment_agreement

        self.create = async_to_streamed_response_wrapper(
            payment_agreement.create,
        )
        self.eligibility = async_to_streamed_response_wrapper(
            payment_agreement.eligibility,
        )
