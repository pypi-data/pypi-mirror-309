# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["InboundResponse", "Data", "DataFeeDetail", "DataFeeDetailFees"]


class DataFeeDetailFees(BaseModel):
    amount: str
    """transfered amount"""

    units: Optional[str] = None


class DataFeeDetail(BaseModel):
    fee_fri: str = FieldInfo(alias="feeFri")

    fees: DataFeeDetailFees

    quote_id: str = FieldInfo(alias="quoteId")
    """427842"""


class Data(BaseModel):
    fee_details: Optional[List[DataFeeDetail]] = FieldInfo(alias="feeDetails", default=None)

    provider_transaction_id: Optional[str] = FieldInfo(alias="providerTransactionId", default=None)

    status_code: Optional[str] = FieldInfo(alias="statusCode", default=None)
    """message"""

    status_message: Optional[str] = FieldInfo(alias="statusMessage", default=None)


class InboundResponse(BaseModel):
    data: Data

    error: str

    status_code: str = FieldInfo(alias="statusCode")
    """
    This is the MADAPI Canonical Error Code (it is 4 characters long and it is not
    the HTTP Status Code which is 3 characters long). Back-end system errors are
    mapped to specific canonical error codes which are returned. 0000 is for a
    success. More information on these mappings can be found on the MADAPI
    Confluence Page 'Response Codes'
    """

    sequence_no: Optional[str] = FieldInfo(alias="sequenceNo", default=None)
    """A unique id for tracing all requests"""
