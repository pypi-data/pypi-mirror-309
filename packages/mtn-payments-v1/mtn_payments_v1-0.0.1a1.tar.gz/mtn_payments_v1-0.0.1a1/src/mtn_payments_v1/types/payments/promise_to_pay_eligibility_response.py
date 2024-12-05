# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PromiseToPayEligibilityResponse", "Data", "DataPromiseToPayEligibilityDetails"]


class DataPromiseToPayEligibilityDetails(BaseModel):
    account_balance: Optional[str] = FieldInfo(alias="accountBalance", default=None)
    """Entire Outstanding amount of the account"""

    eligibility_status: Optional[str] = FieldInfo(alias="eligibilityStatus", default=None)
    """Promise to pay eligibility status.

    Possible status values are ‘Eligible’, ‘Not-eligible’.
    """

    minimum_amount: Optional[str] = FieldInfo(alias="minimumAmount", default=None)
    """Applies NRT_THRESHOLD_VALUE on account balance and returns as the minimumAmount"""

    payment_start_date: Optional[str] = FieldInfo(alias="paymentStartDate", default=None)
    """Payment Start Date holds API triggered date (DD-MM-YYYY)"""


class Data(BaseModel):
    promise_to_pay_eligibility_details: Optional[DataPromiseToPayEligibilityDetails] = FieldInfo(
        alias="PromiseToPayEligibilityDetails", default=None
    )
    """Payment Request eligibility details."""


class PromiseToPayEligibilityResponse(BaseModel):
    data: Optional[Data] = None

    status_code: Optional[str] = FieldInfo(alias="statusCode", default=None)
    """
    This is the MADAPI Canonical Error Code (it is 4 characters long and it is not
    the HTTP Status Code which is 3 characters long). Back-end system errors are
    mapped to specific canonical error codes which are returned. 0000 is for a
    success. More information on these mappings can be found on the MADAPI
    Confluence Page 'Response Codes'
    """

    status_message: Optional[str] = FieldInfo(alias="statusMessage", default=None)
    """Message of the transaction. Either Success or Failure."""

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)
    """Unique identifier for every request to the backend. Mapped from input request."""
