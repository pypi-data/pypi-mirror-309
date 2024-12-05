# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PromiseToPayResponse", "_Links", "_LinksSelf", "Data", "DataPromiseDetail"]


class _LinksSelf(BaseModel):
    href: Optional[str] = None
    """Hyperlink to access the payment agreement generation endpoint."""


class _Links(BaseModel):
    self: Optional[_LinksSelf] = None


class DataPromiseDetail(BaseModel):
    installment_due_amount: Optional[str] = FieldInfo(alias="installmentDueAmount", default=None)
    """Installment Amount Due to be paid"""

    installment_end_date: Optional[datetime] = FieldInfo(alias="installmentEndDate", default=None)
    """End date of Installment"""

    installment_start_date: Optional[datetime] = FieldInfo(alias="installmentStartDate", default=None)
    """Start Date of Installment"""

    query_number: Optional[str] = FieldInfo(alias="queryNumber", default=None)
    """Query Number in SV"""


class Data(BaseModel):
    promise_details: Optional[List[DataPromiseDetail]] = FieldInfo(alias="PromiseDetails", default=None)


class PromiseToPayResponse(BaseModel):
    api_links: Optional[_Links] = FieldInfo(alias="_links", default=None)

    data: Optional[Data] = None

    sequence_no: Optional[str] = FieldInfo(alias="sequenceNo", default=None)
    """A unique id for tracing all requests"""

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
