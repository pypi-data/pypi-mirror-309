# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["HistoryListParams"]


class HistoryListParams(TypedDict, total=False):
    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """End date of the history range"""

    id_type: Annotated[Literal["MSISDN", "USER"], PropertyInfo(alias="idType")]
    """Type of the customerId in the path."""

    node_id: Annotated[str, PropertyInfo(alias="nodeId")]
    """Node making the request"""

    page_number: Annotated[float, PropertyInfo(alias="pageNumber")]
    """Current page or offset number"""

    page_size: Annotated[float, PropertyInfo(alias="pageSize")]
    """Maximum number of items to get from the backend system"""

    query_type: Annotated[str, PropertyInfo(alias="queryType")]
    """Type of request"""

    registration_channel: Annotated[str, PropertyInfo(alias="registrationChannel")]
    """Channel making the request"""

    request_type: Annotated[Literal["MOMO"], PropertyInfo(alias="requestType")]
    """type of request"""

    segment: Literal["subscriber", "agent", "merchant", "admin"]
    """Segment of the customer.

    For example, subscriber,agent, merchant, admin depending on the type of customer
    whome the operation is being performed against.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Start date of the history range"""

    start_time: Annotated[str, PropertyInfo(alias="startTime")]
    """
    Start time of the transaction.If blank, then transaction received date will be
    set as start time
    """

    status: str
    """Status of the transactions"""

    target_system: Annotated[Literal["CPG", "EWP"], PropertyInfo(alias="targetSystem")]
    """target system expected to fulful the service"""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """Unique identifier from the caller"""

    transaction_id: Annotated[str, PropertyInfo(alias="transactionId")]

    x_authorization: Annotated[str, PropertyInfo(alias="X-Authorization")]
