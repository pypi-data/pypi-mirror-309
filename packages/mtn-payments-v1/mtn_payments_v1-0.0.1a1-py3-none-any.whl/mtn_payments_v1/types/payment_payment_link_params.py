# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PaymentPaymentLinkParams"]


class PaymentPaymentLinkParams(TypedDict, total=False):
    body: Required[object]
    """Order Request details."""

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]
