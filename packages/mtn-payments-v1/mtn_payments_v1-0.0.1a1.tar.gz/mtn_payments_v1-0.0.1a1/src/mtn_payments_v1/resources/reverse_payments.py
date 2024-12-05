# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import reverse_payment_history_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.reverse_transaction_history import ReverseTransactionHistory

__all__ = ["ReversePaymentsResource", "AsyncReversePaymentsResource"]


class ReversePaymentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ReversePaymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return ReversePaymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReversePaymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return ReversePaymentsResourceWithStreamingResponse(self)

    def history(
        self,
        *,
        transactiontype: str,
        customer_id: str,
        amount: float | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        node_id: str | NotGiven = NOT_GIVEN,
        other_fri: str | NotGiven = NOT_GIVEN,
        page_no: int | NotGiven = NOT_GIVEN,
        pos_msisdn: str | NotGiven = NOT_GIVEN,
        quote_id: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        correlator_id: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        transactionstatus: str | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReverseTransactionHistory:
        """
        Provides the status of a Payment Transaction to service providers.

        Args:
          transactiontype: transactiontype

          amount: amount of the transaction

          end_date: Retrieve transaction history created until this stop date.

          limit: The maximum number of items to return in the response. Default value 50.

          node_id: Third parties unique identifier. Can also be called channelId.

          other_fri: The FRI of the other party in transaction, could be from or to depending on
              direction. Validated with IsFRI.

          page_no: indexoffset the list of results returned by an API. Optional, If its not
              specified we should return all the values.

          pos_msisdn: Retrieve transaction history performed be the specified point of sale MSISDN.

          quote_id: List all information based on quoteId then quoteId used.

          start_date: Retrieve transaction history created from this start date.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "customerId": customer_id,
                    "correlatorId": correlator_id,
                    "transactionId": transaction_id,
                    "transactionstatus": transactionstatus,
                    "X-Authorization": x_authorization,
                }
            ),
            **(extra_headers or {}),
        }
        return self._get(
            "/reverse-payment/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "transactiontype": transactiontype,
                        "amount": amount,
                        "end_date": end_date,
                        "limit": limit,
                        "node_id": node_id,
                        "other_fri": other_fri,
                        "page_no": page_no,
                        "pos_msisdn": pos_msisdn,
                        "quote_id": quote_id,
                        "start_date": start_date,
                    },
                    reverse_payment_history_params.ReversePaymentHistoryParams,
                ),
            ),
            cast_to=ReverseTransactionHistory,
        )


class AsyncReversePaymentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncReversePaymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return AsyncReversePaymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReversePaymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return AsyncReversePaymentsResourceWithStreamingResponse(self)

    async def history(
        self,
        *,
        transactiontype: str,
        customer_id: str,
        amount: float | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        node_id: str | NotGiven = NOT_GIVEN,
        other_fri: str | NotGiven = NOT_GIVEN,
        page_no: int | NotGiven = NOT_GIVEN,
        pos_msisdn: str | NotGiven = NOT_GIVEN,
        quote_id: str | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        correlator_id: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        transactionstatus: str | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReverseTransactionHistory:
        """
        Provides the status of a Payment Transaction to service providers.

        Args:
          transactiontype: transactiontype

          amount: amount of the transaction

          end_date: Retrieve transaction history created until this stop date.

          limit: The maximum number of items to return in the response. Default value 50.

          node_id: Third parties unique identifier. Can also be called channelId.

          other_fri: The FRI of the other party in transaction, could be from or to depending on
              direction. Validated with IsFRI.

          page_no: indexoffset the list of results returned by an API. Optional, If its not
              specified we should return all the values.

          pos_msisdn: Retrieve transaction history performed be the specified point of sale MSISDN.

          quote_id: List all information based on quoteId then quoteId used.

          start_date: Retrieve transaction history created from this start date.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "customerId": customer_id,
                    "correlatorId": correlator_id,
                    "transactionId": transaction_id,
                    "transactionstatus": transactionstatus,
                    "X-Authorization": x_authorization,
                }
            ),
            **(extra_headers or {}),
        }
        return await self._get(
            "/reverse-payment/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "transactiontype": transactiontype,
                        "amount": amount,
                        "end_date": end_date,
                        "limit": limit,
                        "node_id": node_id,
                        "other_fri": other_fri,
                        "page_no": page_no,
                        "pos_msisdn": pos_msisdn,
                        "quote_id": quote_id,
                        "start_date": start_date,
                    },
                    reverse_payment_history_params.ReversePaymentHistoryParams,
                ),
            ),
            cast_to=ReverseTransactionHistory,
        )


class ReversePaymentsResourceWithRawResponse:
    def __init__(self, reverse_payments: ReversePaymentsResource) -> None:
        self._reverse_payments = reverse_payments

        self.history = to_raw_response_wrapper(
            reverse_payments.history,
        )


class AsyncReversePaymentsResourceWithRawResponse:
    def __init__(self, reverse_payments: AsyncReversePaymentsResource) -> None:
        self._reverse_payments = reverse_payments

        self.history = async_to_raw_response_wrapper(
            reverse_payments.history,
        )


class ReversePaymentsResourceWithStreamingResponse:
    def __init__(self, reverse_payments: ReversePaymentsResource) -> None:
        self._reverse_payments = reverse_payments

        self.history = to_streamed_response_wrapper(
            reverse_payments.history,
        )


class AsyncReversePaymentsResourceWithStreamingResponse:
    def __init__(self, reverse_payments: AsyncReversePaymentsResource) -> None:
        self._reverse_payments = reverse_payments

        self.history = async_to_streamed_response_wrapper(
            reverse_payments.history,
        )
