# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["PaymentAgreementEligibilityParams"]


class PaymentAgreementEligibilityParams(TypedDict, total=False):
    billing_account_number: Required[Annotated[str, PropertyInfo(alias="billingAccountNumber")]]
    """Singleview billing account number."""

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]
