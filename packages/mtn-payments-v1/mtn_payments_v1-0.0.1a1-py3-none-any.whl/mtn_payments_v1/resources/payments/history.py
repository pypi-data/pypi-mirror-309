# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

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
from ...types.payments import history_list_params
from ...types.payments.payment_history_response import PaymentHistoryResponse

__all__ = ["HistoryResource", "AsyncHistoryResource"]


class HistoryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HistoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return HistoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HistoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return HistoryResourceWithStreamingResponse(self)

    def list(
        self,
        id: str,
        *,
        end_date: str | NotGiven = NOT_GIVEN,
        id_type: Literal["MSISDN", "USER"] | NotGiven = NOT_GIVEN,
        node_id: str | NotGiven = NOT_GIVEN,
        page_number: float | NotGiven = NOT_GIVEN,
        page_size: float | NotGiven = NOT_GIVEN,
        query_type: str | NotGiven = NOT_GIVEN,
        registration_channel: str | NotGiven = NOT_GIVEN,
        request_type: Literal["MOMO"] | NotGiven = NOT_GIVEN,
        segment: Literal["subscriber", "agent", "merchant", "admin"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        start_time: str | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        target_system: Literal["CPG", "EWP"] | NotGiven = NOT_GIVEN,
        trace_id: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentHistoryResponse:
        """
        Get a list of payments made on a reference or by a customer id

        Args:
          end_date: End date of the history range

          id_type: Type of the customerId in the path.

          node_id: Node making the request

          page_number: Current page or offset number

          page_size: Maximum number of items to get from the backend system

          query_type: Type of request

          registration_channel: Channel making the request

          request_type: type of request

          segment: Segment of the customer. For example, subscriber,agent, merchant, admin
              depending on the type of customer whome the operation is being performed
              against.

          start_date: Start date of the history range

          start_time: Start time of the transaction.If blank, then transaction received date will be
              set as start time

          status: Status of the transactions

          target_system: target system expected to fulful the service

          trace_id: Unique identifier from the caller

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
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
            f"/payments/{id}/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_date": end_date,
                        "id_type": id_type,
                        "node_id": node_id,
                        "page_number": page_number,
                        "page_size": page_size,
                        "query_type": query_type,
                        "registration_channel": registration_channel,
                        "request_type": request_type,
                        "segment": segment,
                        "start_date": start_date,
                        "start_time": start_time,
                        "status": status,
                        "target_system": target_system,
                        "trace_id": trace_id,
                    },
                    history_list_params.HistoryListParams,
                ),
            ),
            cast_to=PaymentHistoryResponse,
        )


class AsyncHistoryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHistoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#accessing-raw-response-data-eg-headers
        """
        return AsyncHistoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHistoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/mtn-payments-v1#with_streaming_response
        """
        return AsyncHistoryResourceWithStreamingResponse(self)

    async def list(
        self,
        id: str,
        *,
        end_date: str | NotGiven = NOT_GIVEN,
        id_type: Literal["MSISDN", "USER"] | NotGiven = NOT_GIVEN,
        node_id: str | NotGiven = NOT_GIVEN,
        page_number: float | NotGiven = NOT_GIVEN,
        page_size: float | NotGiven = NOT_GIVEN,
        query_type: str | NotGiven = NOT_GIVEN,
        registration_channel: str | NotGiven = NOT_GIVEN,
        request_type: Literal["MOMO"] | NotGiven = NOT_GIVEN,
        segment: Literal["subscriber", "agent", "merchant", "admin"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        start_time: str | NotGiven = NOT_GIVEN,
        status: str | NotGiven = NOT_GIVEN,
        target_system: Literal["CPG", "EWP"] | NotGiven = NOT_GIVEN,
        trace_id: str | NotGiven = NOT_GIVEN,
        transaction_id: str | NotGiven = NOT_GIVEN,
        x_authorization: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentHistoryResponse:
        """
        Get a list of payments made on a reference or by a customer id

        Args:
          end_date: End date of the history range

          id_type: Type of the customerId in the path.

          node_id: Node making the request

          page_number: Current page or offset number

          page_size: Maximum number of items to get from the backend system

          query_type: Type of request

          registration_channel: Channel making the request

          request_type: type of request

          segment: Segment of the customer. For example, subscriber,agent, merchant, admin
              depending on the type of customer whome the operation is being performed
              against.

          start_date: Start date of the history range

          start_time: Start time of the transaction.If blank, then transaction received date will be
              set as start time

          status: Status of the transactions

          target_system: target system expected to fulful the service

          trace_id: Unique identifier from the caller

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
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
            f"/payments/{id}/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_date": end_date,
                        "id_type": id_type,
                        "node_id": node_id,
                        "page_number": page_number,
                        "page_size": page_size,
                        "query_type": query_type,
                        "registration_channel": registration_channel,
                        "request_type": request_type,
                        "segment": segment,
                        "start_date": start_date,
                        "start_time": start_time,
                        "status": status,
                        "target_system": target_system,
                        "trace_id": trace_id,
                    },
                    history_list_params.HistoryListParams,
                ),
            ),
            cast_to=PaymentHistoryResponse,
        )


class HistoryResourceWithRawResponse:
    def __init__(self, history: HistoryResource) -> None:
        self._history = history

        self.list = to_raw_response_wrapper(
            history.list,
        )


class AsyncHistoryResourceWithRawResponse:
    def __init__(self, history: AsyncHistoryResource) -> None:
        self._history = history

        self.list = async_to_raw_response_wrapper(
            history.list,
        )


class HistoryResourceWithStreamingResponse:
    def __init__(self, history: HistoryResource) -> None:
        self._history = history

        self.list = to_streamed_response_wrapper(
            history.list,
        )


class AsyncHistoryResourceWithStreamingResponse:
    def __init__(self, history: AsyncHistoryResource) -> None:
        self._history = history

        self.list = async_to_streamed_response_wrapper(
            history.list,
        )
