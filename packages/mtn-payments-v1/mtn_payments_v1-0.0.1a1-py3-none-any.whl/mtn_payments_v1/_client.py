# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, MtnPaymentsV1Error
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "MtnPaymentsV1",
    "AsyncMtnPaymentsV1",
    "Client",
    "AsyncClient",
]


class MtnPaymentsV1(SyncAPIClient):
    payments: resources.PaymentsResource
    reverse_payments: resources.ReversePaymentsResource
    with_raw_response: MtnPaymentsV1WithRawResponse
    with_streaming_response: MtnPaymentsV1WithStreamedResponse

    # client options
    client_id: str
    client_secret: str

    def __init__(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous mtn-payments-v1 client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `client_id` from `OAUTH_CLIENT_ID`
        - `client_secret` from `OAUTH_CLIENT_SECRET`
        """
        if client_id is None:
            client_id = os.environ.get("OAUTH_CLIENT_ID")
        if client_id is None:
            raise MtnPaymentsV1Error(
                "The client_id client option must be set either by passing client_id to the client or by setting the OAUTH_CLIENT_ID environment variable"
            )
        self.client_id = client_id

        if client_secret is None:
            client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
        if client_secret is None:
            raise MtnPaymentsV1Error(
                "The client_secret client option must be set either by passing client_secret to the client or by setting the OAUTH_CLIENT_SECRET environment variable"
            )
        self.client_secret = client_secret

        if base_url is None:
            base_url = os.environ.get("MTN_PAYMENTS_V1_BASE_URL")
        if base_url is None:
            base_url = f"https://api.mtn.com/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.payments = resources.PaymentsResource(self)
        self.reverse_payments = resources.ReversePaymentsResource(self)
        self.with_raw_response = MtnPaymentsV1WithRawResponse(self)
        self.with_streaming_response = MtnPaymentsV1WithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            client_id=client_id or self.client_id,
            client_secret=client_secret or self.client_secret,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncMtnPaymentsV1(AsyncAPIClient):
    payments: resources.AsyncPaymentsResource
    reverse_payments: resources.AsyncReversePaymentsResource
    with_raw_response: AsyncMtnPaymentsV1WithRawResponse
    with_streaming_response: AsyncMtnPaymentsV1WithStreamedResponse

    # client options
    client_id: str
    client_secret: str

    def __init__(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async mtn-payments-v1 client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `client_id` from `OAUTH_CLIENT_ID`
        - `client_secret` from `OAUTH_CLIENT_SECRET`
        """
        if client_id is None:
            client_id = os.environ.get("OAUTH_CLIENT_ID")
        if client_id is None:
            raise MtnPaymentsV1Error(
                "The client_id client option must be set either by passing client_id to the client or by setting the OAUTH_CLIENT_ID environment variable"
            )
        self.client_id = client_id

        if client_secret is None:
            client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
        if client_secret is None:
            raise MtnPaymentsV1Error(
                "The client_secret client option must be set either by passing client_secret to the client or by setting the OAUTH_CLIENT_SECRET environment variable"
            )
        self.client_secret = client_secret

        if base_url is None:
            base_url = os.environ.get("MTN_PAYMENTS_V1_BASE_URL")
        if base_url is None:
            base_url = f"https://api.mtn.com/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.payments = resources.AsyncPaymentsResource(self)
        self.reverse_payments = resources.AsyncReversePaymentsResource(self)
        self.with_raw_response = AsyncMtnPaymentsV1WithRawResponse(self)
        self.with_streaming_response = AsyncMtnPaymentsV1WithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            client_id=client_id or self.client_id,
            client_secret=client_secret or self.client_secret,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class MtnPaymentsV1WithRawResponse:
    def __init__(self, client: MtnPaymentsV1) -> None:
        self.payments = resources.PaymentsResourceWithRawResponse(client.payments)
        self.reverse_payments = resources.ReversePaymentsResourceWithRawResponse(client.reverse_payments)


class AsyncMtnPaymentsV1WithRawResponse:
    def __init__(self, client: AsyncMtnPaymentsV1) -> None:
        self.payments = resources.AsyncPaymentsResourceWithRawResponse(client.payments)
        self.reverse_payments = resources.AsyncReversePaymentsResourceWithRawResponse(client.reverse_payments)


class MtnPaymentsV1WithStreamedResponse:
    def __init__(self, client: MtnPaymentsV1) -> None:
        self.payments = resources.PaymentsResourceWithStreamingResponse(client.payments)
        self.reverse_payments = resources.ReversePaymentsResourceWithStreamingResponse(client.reverse_payments)


class AsyncMtnPaymentsV1WithStreamedResponse:
    def __init__(self, client: AsyncMtnPaymentsV1) -> None:
        self.payments = resources.AsyncPaymentsResourceWithStreamingResponse(client.payments)
        self.reverse_payments = resources.AsyncReversePaymentsResourceWithStreamingResponse(client.reverse_payments)


Client = MtnPaymentsV1

AsyncClient = AsyncMtnPaymentsV1
