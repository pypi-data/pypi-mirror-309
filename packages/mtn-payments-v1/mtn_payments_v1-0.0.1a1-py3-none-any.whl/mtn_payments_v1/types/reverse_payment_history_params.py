# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ReversePaymentHistoryParams"]


class ReversePaymentHistoryParams(TypedDict, total=False):
    transactiontype: Required[str]
    """transactiontype"""

    customer_id: Required[Annotated[str, PropertyInfo(alias="customerId")]]

    amount: float
    """amount of the transaction"""

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """Retrieve transaction history created until this stop date."""

    limit: int
    """The maximum number of items to return in the response. Default value 50."""

    node_id: Annotated[str, PropertyInfo(alias="nodeId")]
    """Third parties unique identifier. Can also be called channelId."""

    other_fri: Annotated[str, PropertyInfo(alias="otherFri")]
    """
    The FRI of the other party in transaction, could be from or to depending on
    direction. Validated with IsFRI.
    """

    page_no: Annotated[int, PropertyInfo(alias="pageNo")]
    """indexoffset the list of results returned by an API.

    Optional, If its not specified we should return all the values.
    """

    pos_msisdn: Annotated[str, PropertyInfo(alias="posMsisdn")]
    """Retrieve transaction history performed be the specified point of sale MSISDN."""

    quote_id: Annotated[str, PropertyInfo(alias="quoteId")]
    """List all information based on quoteId then quoteId used."""

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Retrieve transaction history created from this start date."""

    correlator_id: Annotated[str, PropertyInfo(alias="correlatorId")]

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]

    transactionstatus: str

    x_authorization: Annotated[str, PropertyInfo(alias="X-Authorization")]
