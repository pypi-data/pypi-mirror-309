# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PaymentTransactionStatusParams"]


class PaymentTransactionStatusParams(TypedDict, total=False):
    amount: float

    customer_id: Annotated[str, PropertyInfo(alias="customerId")]
    """This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN"""

    description: str
    """can be a payer note, a merchant identifier ie. merchantId etc."""

    payment_type: Annotated[Literal["Airtime"], PropertyInfo(alias="paymentType")]
    """Type of the transaction"""

    target_system: Annotated[Literal["EWP", "ECW", "CELD"], PropertyInfo(alias="targetSystem")]
    """target system expected to fulful the service"""

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]

    x_authorization: Annotated[str, PropertyInfo(alias="X-Authorization")]
