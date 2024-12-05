# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["PaymentAgreementCreateParams"]


class PaymentAgreementCreateParams(TypedDict, total=False):
    billing_account_no: Annotated[str, PropertyInfo(alias="billingAccountNo")]
    """Unique Billing Account number of the customer"""

    duration_uom: Annotated[str, PropertyInfo(alias="durationUOM")]
    """Unit of Measure for the EMI (can be Month, Week and Year)."""

    number_of_installments: Annotated[str, PropertyInfo(alias="numberOfInstallments")]
    """Number of the EMI."""

    promise_amount: Annotated[float, PropertyInfo(alias="promiseAmount")]
    """Amount promised to be paid."""

    promise_open_date: Annotated[Union[str, datetime], PropertyInfo(alias="promiseOpenDate", format="iso8601")]
    """Start Date of the Promise."""

    promise_threshold: Annotated[str, PropertyInfo(alias="promiseThreshold")]
    """The Promise Threshold"""

    service_name: Annotated[str, PropertyInfo(alias="serviceName")]
    """Service name of the payment."""

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]
