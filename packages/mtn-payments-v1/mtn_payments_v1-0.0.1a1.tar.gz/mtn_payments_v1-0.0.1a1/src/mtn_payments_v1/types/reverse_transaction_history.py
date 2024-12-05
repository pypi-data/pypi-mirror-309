# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ReverseTransactionHistory",
    "_Links",
    "_LinksSelf",
    "Data",
    "DataAmount",
    "DataExternalamount",
    "DataFromamount",
    "DataFromavailablebalance",
    "DataFromcommittedbalance",
    "DataFromcouponvalue",
    "DataFromdiscount",
    "DataFromexternalfee",
    "DataFromfee",
    "DataFromfeerefund",
    "DataFromloyfee",
    "DataFromloyreward",
    "DataFrompromotion",
    "DataFrompromotionrefund",
    "DataFromtaxes",
    "DataFromtaxesrefund",
    "DataFromtotalbalance",
    "DataOriginalamount",
    "DataToamount",
    "DataToavailablebalance",
    "DataTocommittedbalance",
    "DataTodiscountrefund",
    "DataToexternalfee",
    "DataTofee",
    "DataTofeerefund",
    "DataToloyfee",
    "DataToloyreward",
    "DataTopromotion",
    "DataTopromotionrefund",
    "DataTotaxes",
    "DataTotaxesrefund",
    "DataTototalbalance",
    "LoyaltyInformation",
    "LoyaltyInformationConsumedAmount",
    "LoyaltyInformationGeneratedAmount",
    "LoyaltyInformationNewBalance",
]


class _LinksSelf(BaseModel):
    href: Optional[str] = None
    """Hyperlink to access the financial payment."""


class _Links(BaseModel):
    self: Optional[_LinksSelf] = None


class DataAmount(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataExternalamount(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromamount(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromavailablebalance(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromcommittedbalance(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromcouponvalue(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromdiscount(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromexternalfee(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromfee(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromfeerefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromloyfee(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromloyreward(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFrompromotion(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFrompromotionrefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromtaxes(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromtaxesrefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataFromtotalbalance(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataOriginalamount(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataToamount(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataToavailablebalance(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTocommittedbalance(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTodiscountrefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataToexternalfee(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTofee(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTofeerefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataToloyfee(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataToloyreward(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTopromotion(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTopromotionrefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTotaxes(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTotaxesrefund(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class DataTototalbalance(BaseModel):
    amount: float
    """Amount of money"""

    currency: str
    """Currency"""


class Data(BaseModel):
    amount: Optional[DataAmount] = None
    """Representation of monetary value."""

    commitdate: Optional[str] = None
    """The date and time at which the transaction was completed."""

    communicationchannel: Optional[str] = None
    """The communication channel.."""

    externalamount: Optional[DataExternalamount] = None
    """Representation of monetary value."""

    externalfxrate: Optional[str] = None
    """The external foreign exchange rate in an interoperability transfer."""

    externalserviceprovider: Optional[str] = None
    """The external service provider that was involved in the transaction.."""

    external_svc_prd_tran_id: Optional[str] = FieldInfo(alias="externalSvcPrdTranId", default=None)
    """The transaction ID generated by an external service provider.

    This field is only available when searching for a specific transaction by
    financialTransactionId or externalTransactionId.
    """

    externaltransactionid: Optional[str] = None
    """External transaction ID for the operation.."""

    fitype: Optional[str] = None
    """Shows the financial transaction type."""

    from_: Optional[str] = FieldInfo(alias="from", default=None)
    """The sending user's default FRI."""

    fromaccount: Optional[str] = None
    """The sending account FRI."""

    fromaccountholder: Optional[str] = None
    """The identity of the sending account holder."""

    fromamount: Optional[DataFromamount] = None
    """Representation of monetary value."""

    fromavailablebalance: Optional[DataFromavailablebalance] = None
    """Representation of monetary value."""

    fromcommittedbalance: Optional[DataFromcommittedbalance] = None
    """Representation of monetary value."""

    fromcouponvalue: Optional[DataFromcouponvalue] = None
    """Representation of monetary value."""

    fromdiscount: Optional[DataFromdiscount] = None
    """Representation of monetary value."""

    from_ex_instru_acc_holder: Optional[str] = FieldInfo(alias="fromExInstruAccHolder", default=None)
    """
    The external instrument provider account holder if the sending FRI is an
    external instrument. This field is only available when searching for a specific
    transaction by financialTransactionId or externalTransactionId.
    """

    from_ex_instru_prov_trans_id: Optional[str] = FieldInfo(alias="fromExInstruProvTransId", default=None)
    """
    The external transaction identifier as provided by the external instrument
    provider if the sending FRI is an external instrument. This field is only
    available when searching for a specific transaction by financialTransactionId or
    externalTransactionId..
    """

    fromexternalfee: Optional[DataFromexternalfee] = None
    """Representation of monetary value."""

    fromfee: Optional[DataFromfee] = None
    """Representation of monetary value."""

    fromfeerefund: Optional[DataFromfeerefund] = None
    """Representation of monetary value."""

    fromfirstname: Optional[str] = None
    """The first name of the sender."""

    fromhandlerfirstname: Optional[str] = None
    """The first name of the handler on the sender side."""

    fromhandlerlastname: Optional[str] = None
    """The last name of the handler on the sender side."""

    fromlastname: Optional[str] = None
    """The last name of the sender."""

    fromloyfee: Optional[DataFromloyfee] = None
    """Representation of monetary value."""

    fromloyreward: Optional[DataFromloyreward] = None
    """Representation of monetary value."""

    fromnote: Optional[str] = None
    """The sender's note.."""

    fromposmsisdn: Optional[str] = None
    """The point of sale msisdn of the sender."""

    frompromotion: Optional[DataFrompromotion] = None
    """Representation of monetary value."""

    frompromotionrefund: Optional[DataFrompromotionrefund] = None
    """Representation of monetary value."""

    fromtaxes: Optional[DataFromtaxes] = None
    """Representation of monetary value."""

    fromtaxesrefund: Optional[DataFromtaxesrefund] = None
    """Representation of monetary value."""

    fromtotalbalance: Optional[DataFromtotalbalance] = None
    """Representation of monetary value."""

    fxrate: Optional[str] = None
    """The foreign exchange rate."""

    initiatingaccountholder: Optional[str] = None
    """
    The Identity of the account holder that initiated the transaction if it was
    initiated by an account holder.
    """

    initiatinguser: Optional[str] = None
    """The execution ID of the user that initiated the transaction."""

    instructionid: Optional[str] = None
    """The financial instruction ID.."""

    maininstructionid: Optional[str] = None
    """The main instruction ID."""

    originalamount: Optional[DataOriginalamount] = None
    """Representation of monetary value."""

    originaltransactionid: Optional[str] = None
    """The original transaction id.."""

    providercategory: Optional[str] = None
    """The name of the provider category."""

    realaccountholder: Optional[str] = None
    """
    The Identity of the real account holder that is effected by the transaction if
    it was initiated by an account holder.
    """

    realuser: Optional[str] = None
    """The execution ID of the real user that initiated the transaction."""

    reviewinguser: Optional[str] = None
    """The execution ID of the user that reviewed the transaction."""

    startdate: Optional[str] = None
    """Select transactions starting from this date and time."""

    to: Optional[str] = None
    """The receiving user's FRI or the receiving account's FRI."""

    toaccount: Optional[str] = None
    """The receiving account's FRI."""

    toaccountholder: Optional[str] = None
    """The Identity of the receiving account holder."""

    toamount: Optional[DataToamount] = None
    """Representation of monetary value."""

    toavailablebalance: Optional[DataToavailablebalance] = None
    """Representation of monetary value."""

    tocommittedbalance: Optional[DataTocommittedbalance] = None
    """Representation of monetary value."""

    todiscountrefund: Optional[DataTodiscountrefund] = None
    """Representation of monetary value."""

    to_ex_instru_acc_holder: Optional[str] = FieldInfo(alias="toExInstruAccHolder", default=None)
    """
    The external instrument provider account holder if the receiving FRI is an
    external instrument. This field is only available when searching for a specific
    transaction by financialTransactionId or externalTransactionId.
    """

    to_ex_instru_prov_trans_id: Optional[str] = FieldInfo(alias="toExInstruProvTransId", default=None)
    """
    The external transaction identifier as provided by the external instrument
    provider if the receiving FRI is an external instrument. This field is only
    available when searching for a specific transaction by financialTransactionId or
    externalTransactionId.
    """

    toexternalfee: Optional[DataToexternalfee] = None
    """Representation of monetary value."""

    tofee: Optional[DataTofee] = None
    """Representation of monetary value."""

    tofeerefund: Optional[DataTofeerefund] = None
    """Representation of monetary value."""

    tofirstname: Optional[str] = None
    """The first name of receiver."""

    tohandlerfirstname: Optional[str] = None
    """The first name of the handler on the receiver side."""

    tohandlerlastname: Optional[str] = None
    """The last name of the handler on the receiver side."""

    tolastname: Optional[str] = None
    """The last name of the receiver."""

    toloyfee: Optional[DataToloyfee] = None
    """Representation of monetary value."""

    toloyreward: Optional[DataToloyreward] = None
    """Representation of monetary value."""

    tomessage: Optional[str] = None
    """The receiver's message."""

    toposmsisdn: Optional[str] = None
    """The point of sale msisdn of the receiver."""

    topromotion: Optional[DataTopromotion] = None
    """Representation of monetary value."""

    topromotionrefund: Optional[DataTopromotionrefund] = None
    """Representation of monetary value."""

    totaxes: Optional[DataTotaxes] = None
    """Representation of monetary value."""

    totaxesrefund: Optional[DataTotaxesrefund] = None
    """Representation of monetary value."""

    tototalbalance: Optional[DataTototalbalance] = None
    """Representation of monetary value."""

    transactionstatus: Optional[str] = None
    """SUCCESSFULL."""

    transactiontext: Optional[str] = None
    """Text describing the transaction.."""

    transfertype: Optional[str] = None
    """TRANSFER."""


class LoyaltyInformationConsumedAmount(BaseModel):
    amount: float
    """Amount of money"""

    units: str
    """Currency"""


class LoyaltyInformationGeneratedAmount(BaseModel):
    amount: float
    """Amount of money"""

    units: str
    """Currency"""


class LoyaltyInformationNewBalance(BaseModel):
    amount: float
    """Amount of money"""

    units: str
    """Currency"""


class LoyaltyInformation(BaseModel):
    consumed_amount: Optional[LoyaltyInformationConsumedAmount] = FieldInfo(alias="consumedAmount", default=None)
    """Representation of monetary value."""

    generated_amount: Optional[LoyaltyInformationGeneratedAmount] = FieldInfo(alias="generatedAmount", default=None)
    """Representation of monetary value."""

    new_balance: Optional[LoyaltyInformationNewBalance] = FieldInfo(alias="newBalance", default=None)
    """Representation of monetary value."""


class ReverseTransactionHistory(BaseModel):
    api_links: Optional[_Links] = FieldInfo(alias="_links", default=None)
    """Relevant links to the financial payment."""

    correlator_id: Optional[str] = FieldInfo(alias="correlatorId", default=None)

    data: Optional[Data] = None

    loyalty_information: Optional[LoyaltyInformation] = FieldInfo(alias="loyaltyInformation", default=None)
    """Contains all the loyalty balances associated with a customer."""

    sequence_no: Optional[str] = FieldInfo(alias="sequenceNo", default=None)
    """A unique id for tracing all requests"""

    status_code: Optional[str] = FieldInfo(alias="statusCode", default=None)

    status_message: Optional[str] = FieldInfo(alias="statusMessage", default=None)

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)
    """API generated Id to include for tracing requests"""
