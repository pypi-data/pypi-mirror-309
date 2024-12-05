# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "PaymentHistoryResponse",
    "Data",
    "DataAccount",
    "DataAmount",
    "DataPayer",
    "DataPayerValidFor",
    "DataPaymentItem",
    "DataPaymentItemItem",
    "DataPaymentRecord",
    "DataPaymentRecordAmount",
    "DataPaymentRecordDestinationAmount",
    "DataPaymentRecordDestinationAvailableBalance",
    "DataPaymentRecordDestinationCommittedBalance",
    "DataPaymentRecordDestinationFee",
    "DataPaymentRecordDestinationTotalBalance",
    "DataPaymentRecordDetails",
    "DataPaymentRecordOriginalAmount",
    "DataPaymentRecordOriginatorAmount",
    "DataPaymentRecordOriginatorFee",
    "DataRelatedParty",
    "DataRelatedPartyValidFor",
    "DataTotalAmount",
]


class DataAccount(BaseModel):
    id: Optional[str] = None
    """Unique identifier of the account"""

    description: Optional[str] = None
    """Detailed description of the account"""

    name: Optional[str] = None
    """Name of the account"""


class DataAmount(BaseModel):
    unit: Optional[str] = None
    """Currency (ISO4217 norm uses 3 letters to define the currency)"""

    value: Optional[float] = None
    """A positive floating point number"""


class DataPayerValidFor(BaseModel):
    end_date_time: Optional[datetime] = FieldInfo(alias="endDateTime", default=None)
    """End of the time period, using IETC-RFC-3339 format"""

    start_date_time: Optional[datetime] = FieldInfo(alias="startDateTime", default=None)
    """Start of the time period, using IETC-RFC-3339 format.

    If you define a start, you must also define an end
    """


class DataPayer(BaseModel):
    id: Optional[str] = None
    """Unique identifier of a related entity."""

    email: Optional[str] = None
    """Email of the related party entity"""

    name: Optional[str] = None
    """Name of the related entity."""

    other_name: Optional[str] = FieldInfo(alias="otherName", default=None)
    """Othername of the related party entity"""

    valid_for: Optional[DataPayerValidFor] = FieldInfo(alias="validFor", default=None)
    """
    A period of time, either as a deadline (endDateTime only) a startDateTime only,
    or both
    """


class DataPaymentItemItem(BaseModel):
    id: Optional[str] = None
    """ID of the item being paid for. This can be a productId"""

    name: Optional[str] = None
    """This is the name of the item being paid for"""


class DataPaymentItem(BaseModel):
    id: Optional[str] = None
    """Unique identifier of the payment Item"""

    item: Optional[DataPaymentItemItem] = None


class DataPaymentRecordAmount(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordDestinationAmount(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordDestinationAvailableBalance(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordDestinationCommittedBalance(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordDestinationFee(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordDestinationTotalBalance(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordDetails(BaseModel):
    brand: Optional[str] = None

    issuer: Optional[str] = None


class DataPaymentRecordOriginalAmount(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordOriginatorAmount(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecordOriginatorFee(BaseModel):
    amount: Optional[str] = None

    unit: Optional[str] = None


class DataPaymentRecord(BaseModel):
    amount: Optional[DataPaymentRecordAmount] = None

    channel: Optional[str] = None

    commit_date: Optional[str] = FieldInfo(alias="commitDate", default=None)

    description: Optional[str] = None

    destination: Optional[str] = None

    destination_account: Optional[str] = FieldInfo(alias="destinationAccount", default=None)

    destination_account_holder: Optional[str] = FieldInfo(alias="destinationAccountHolder", default=None)

    destination_amount: Optional[DataPaymentRecordDestinationAmount] = FieldInfo(
        alias="destinationAmount", default=None
    )

    destination_available_balance: Optional[DataPaymentRecordDestinationAvailableBalance] = FieldInfo(
        alias="destinationAvailableBalance", default=None
    )

    destination_committed_balance: Optional[DataPaymentRecordDestinationCommittedBalance] = FieldInfo(
        alias="destinationCommittedBalance", default=None
    )

    destination_fee: Optional[DataPaymentRecordDestinationFee] = FieldInfo(alias="destinationFee", default=None)

    destination_first_name: Optional[str] = FieldInfo(alias="destinationFirstName", default=None)

    destination_handler_first_name: Optional[str] = FieldInfo(alias="destinationHandlerFirstName", default=None)

    destination_handler_last_name: Optional[str] = FieldInfo(alias="destinationHandlerLastName", default=None)

    destination_last_name: Optional[str] = FieldInfo(alias="destinationLastName", default=None)

    destination_total_balance: Optional[DataPaymentRecordDestinationTotalBalance] = FieldInfo(
        alias="destinationTotalBalance", default=None
    )

    details: Optional[DataPaymentRecordDetails] = None

    fulfillment_status: Optional[str] = FieldInfo(alias="fulfillmentStatus", default=None)

    fx_rate: Optional[str] = FieldInfo(alias="fxRate", default=None)

    initiating_account_holder: Optional[str] = FieldInfo(alias="initiatingAccountHolder", default=None)

    initiating_user: Optional[str] = FieldInfo(alias="initiatingUser", default=None)

    instruction_id: Optional[str] = FieldInfo(alias="instructionId", default=None)

    main_instruction_id: Optional[str] = FieldInfo(alias="mainInstructionId", default=None)

    original_amount: Optional[DataPaymentRecordOriginalAmount] = FieldInfo(alias="originalAmount", default=None)

    originator: Optional[str] = None

    originator_account: Optional[str] = FieldInfo(alias="originatorAccount", default=None)

    originator_account_holder: Optional[str] = FieldInfo(alias="originatorAccountHolder", default=None)

    originator_amount: Optional[DataPaymentRecordOriginatorAmount] = FieldInfo(alias="originatorAmount", default=None)

    originator_fee: Optional[DataPaymentRecordOriginatorFee] = FieldInfo(alias="originatorFee", default=None)

    originator_first_name: Optional[str] = FieldInfo(alias="originatorFirstName", default=None)

    originator_handler_first_name: Optional[str] = FieldInfo(alias="originatorHandlerFirstName", default=None)

    originator_handler_last_name: Optional[str] = FieldInfo(alias="originatorHandlerLastName", default=None)

    originator_last_name: Optional[str] = FieldInfo(alias="originatorLastName", default=None)

    payment_date: Optional[str] = FieldInfo(alias="paymentDate", default=None)

    payment_id: Optional[str] = FieldInfo(alias="paymentId", default=None)

    payment_type: Optional[str] = FieldInfo(alias="paymentType", default=None)

    real_account_holder: Optional[str] = FieldInfo(alias="realAccountHolder", default=None)

    real_user: Optional[str] = FieldInfo(alias="realUser", default=None)

    status: Optional[str] = None

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)


class DataRelatedPartyValidFor(BaseModel):
    end_date_time: Optional[datetime] = FieldInfo(alias="endDateTime", default=None)
    """End of the time period, using IETC-RFC-3339 format"""

    start_date_time: Optional[datetime] = FieldInfo(alias="startDateTime", default=None)
    """Start of the time period, using IETC-RFC-3339 format.

    If you define a start, you must also define an end
    """


class DataRelatedParty(BaseModel):
    id: Optional[str] = None
    """Unique identifier of a related entity."""

    email: Optional[str] = None
    """Email of the related party entity"""

    name: Optional[str] = None
    """Name of the related entity."""

    other_name: Optional[str] = FieldInfo(alias="otherName", default=None)
    """Othername of the related party entity"""

    valid_for: Optional[DataRelatedPartyValidFor] = FieldInfo(alias="validFor", default=None)
    """
    A period of time, either as a deadline (endDateTime only) a startDateTime only,
    or both
    """


class DataTotalAmount(BaseModel):
    unit: Optional[str] = None
    """Currency (ISO4217 norm uses 3 letters to define the currency)"""

    value: Optional[float] = None
    """A positive floating point number"""


class Data(BaseModel):
    id: Optional[str] = None
    """Unique identifier of Payment"""

    account: Optional[DataAccount] = None

    amount: Optional[DataAmount] = None
    """A base / value business entity used to represent money"""

    authorization_code: Optional[str] = FieldInfo(alias="authorizationCode", default=None)
    """
    Authorization code retrieved from an external payment gateway that could be used
    for conciliation
    """

    callback_url: Optional[str] = FieldInfo(alias="callbackUrl", default=None)
    """Callback URL"""

    correlator_id: Optional[str] = FieldInfo(alias="correlatorId", default=None)
    """
    Unique identifier in the client for the payment in case it is needed to
    correlate
    """

    description: Optional[str] = None
    """Text describing the contents of the payment"""

    href: Optional[str] = None
    """Hypertext Reference of the Payment"""

    name: Optional[str] = None
    """Screen name of the payment"""

    payer: Optional[DataPayer] = None
    """Related Entity reference.

    A related party defines party or party role linked to a specific entity.
    """

    payment_date: Optional[datetime] = FieldInfo(alias="paymentDate", default=None)
    """Date when the payment was performed"""

    payment_item: Optional[List[DataPaymentItem]] = FieldInfo(alias="paymentItem", default=None)

    payment_records: Optional[List[DataPaymentRecord]] = FieldInfo(alias="paymentRecords", default=None)

    related_party: Optional[DataRelatedParty] = FieldInfo(alias="relatedParty", default=None)
    """Related Entity reference.

    A related party defines party or party role linked to a specific entity.
    """

    status: Optional[str] = None
    """Status of the payment"""

    status_date: Optional[datetime] = FieldInfo(alias="statusDate", default=None)
    """Date when the status was recorded"""

    total_amount: Optional[DataTotalAmount] = FieldInfo(alias="totalAmount", default=None)
    """A base / value business entity used to represent money"""

    type: Optional[str] = None
    """When sub-classing, this defines the sub-class entity name"""


class PaymentHistoryResponse(BaseModel):
    customer_id: Optional[str] = FieldInfo(alias="customerId", default=None)
    """Customer Id of the customer whose history is being retrieved"""

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
