# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "PaymentFeeParams",
    "PaymentMethod",
    "PaymentMethodDetails",
    "PaymentMethodDetailsAccount",
    "PaymentMethodDetailsBankAccountDebit",
    "PaymentMethodDetailsBankAccountTransfer",
    "PaymentMethodDetailsBankCard",
    "PaymentMethodDetailsBucket",
    "PaymentMethodDetailsDigitalWallet",
    "PaymentMethodDetailsInvoice",
    "PaymentMethodDetailsLoyaltyAccount",
    "PaymentMethodDetailsTokenizedCard",
    "PaymentMethodDetailsVoucher",
    "TotalAmount",
    "AdditionalInformation",
    "Amount",
    "Payee",
    "PayeeTotalAmount",
    "PayeeAmount",
    "PayeeTaxAmount",
    "Payer",
    "TaxAmount",
]


class PaymentFeeParams(TypedDict, total=False):
    callback_url: Required[Annotated[str, PropertyInfo(alias="callbackURL")]]
    """The callback URL."""

    correlator_id: Required[Annotated[str, PropertyInfo(alias="correlatorId")]]
    """
    Unique identifier in the client for the payment in case it is needed to
    correlate, a trace id associated with the caller
    """

    payment_method: Required[Annotated[PaymentMethod, PropertyInfo(alias="paymentMethod")]]
    """Reference or value of the method used to process the payment."""

    total_amount: Required[Annotated[TotalAmount, PropertyInfo(alias="totalAmount")]]
    """Representation of SWZ monetary value."""

    transaction_type: Required[Annotated[str, PropertyInfo(alias="transactionType")]]
    """calling systemn."""

    additional_information: Annotated[Iterable[AdditionalInformation], PropertyInfo(alias="additionalInformation")]

    amount: Amount
    """Representation of SWZ monetary value."""

    authorization_code: Annotated[str, PropertyInfo(alias="authorizationCode")]
    """
    Authorization code retrieved from an external payment gateway that could be used
    for conciliation.
    """

    calling_system: Annotated[str, PropertyInfo(alias="callingSystem")]
    """calling system."""

    channel: str
    """
    The channel used to perform the payment operation or just the channel itself
    with just its name.
    """

    description: str
    """Text describing the contents of the payment."""

    fee_bearer: Annotated[Literal["Payer", "Payee"], PropertyInfo(alias="feeBearer")]
    """Who bears a charge for a particular transaction , whether a Payer or Payee"""

    name: str
    """Screen name of the payment."""

    payee: Iterable[Payee]

    payer: Payer
    """The individual that performs the payment."""

    payment_date: Annotated[Union[str, datetime], PropertyInfo(alias="paymentDate", format="iso8601")]
    """Date when the payment was performed."""

    quote_id: Annotated[str, PropertyInfo(alias="quoteId")]
    """The ID of the quote used, a terminal id associated with the caller."""

    segment: Literal["subscriber", "agent", "merchant", "admin"]
    """Segment of the customer.

    Forexample, subscriber,agent, merchant, admin depending on the type of customer
    whome the operation is being performed against.
    """

    status: str
    """Status of the payment method."""

    status_date: Annotated[Union[str, datetime], PropertyInfo(alias="statusDate", format="iso8601")]
    """Time the status of the payment method changed."""

    target_system: Annotated[str, PropertyInfo(alias="targetSystem")]
    """calling systemn."""

    tax_amount: Annotated[TaxAmount, PropertyInfo(alias="taxAmount")]
    """Representation of SWZ monetary value."""


class PaymentMethodDetailsAccount(TypedDict, total=False):
    id: str
    """Unique identifier of the account."""

    description: str
    """Description of the associated account."""

    name: str
    """Entity name."""


class PaymentMethodDetailsBankAccountDebit(TypedDict, total=False):
    account_number: Annotated[str, PropertyInfo(alias="accountNumber")]
    """Bank Account Number (this could refer to the IBAN or SWIFT number)."""

    account_number_type: Annotated[str, PropertyInfo(alias="accountNumberType")]
    """Type of account number. e.g. IBAN, SWIFT."""

    bank: str
    """Display nam of the bank."""

    bic: Annotated[str, PropertyInfo(alias="BIC")]
    """
    Business Identifier Code/Swift code of the financial institution where the
    account is located.
    """

    owner: str
    """Owner of the bank account."""


class PaymentMethodDetailsBankAccountTransfer(TypedDict, total=False):
    account_number: Annotated[str, PropertyInfo(alias="accountNumber")]
    """Bank Account Number (this could refer to the IBAN or SWIFT number)."""

    account_number_type: Annotated[str, PropertyInfo(alias="accountNumberType")]
    """Type of account number. e.g. IBAN, SWIFT."""

    bank: str
    """Display nam of the bank."""

    bic: Annotated[str, PropertyInfo(alias="BIC")]
    """
    Business Identifier Code/Swift code of the financial institution where the
    account is located.
    """

    owner: str
    """Owner of the bank account."""


class PaymentMethodDetailsBankCard(TypedDict, total=False):
    bank: str
    """Bank that issued the card."""

    brand: str
    """Card brand. e.g. Visa, MasterCard, AmericanExpress."""

    card_number: Annotated[str, PropertyInfo(alias="cardNumber")]
    """Credit card number."""

    cvv: str
    """Security Code of the card. e.g. CCV, CCV2."""

    expiration_date: Annotated[Union[str, datetime], PropertyInfo(alias="expirationDate", format="iso8601")]
    """Expiration date of the card."""

    last_four_digits: Annotated[str, PropertyInfo(alias="lastFourDigits")]
    """Last four digits of the credit card."""

    name_on_card: Annotated[str, PropertyInfo(alias="nameOnCard")]
    """Name on the card."""

    pin: str
    """Customer pin created when tokenizing the card"""

    type: str
    """Type of card. e.g. Credit, Debit."""


class PaymentMethodDetailsBucket(TypedDict, total=False):
    id: str
    """Unique identifier of the bucket."""

    description: str
    """Description of the associated bucket."""

    name: str
    """Entity name."""


class PaymentMethodDetailsDigitalWallet(TypedDict, total=False):
    service: str
    """Organization, platform or currency backing the wallet.

    e.g. MoMo, PayPal, Yandex, BitCoin. Can also be an extension of a service being
    paid for
    """

    wallet_id: Annotated[str, PropertyInfo(alias="walletId")]
    """Account identifier in that service."""

    wallet_uri: Annotated[str, PropertyInfo(alias="walletUri")]
    """URI pointing at the digital wallet."""


class PaymentMethodDetailsInvoice(TypedDict, total=False):
    id: str
    """This is the Id of the invoice"""

    callback_url: Annotated[str, PropertyInfo(alias="callbackUrl")]
    """The url to be invoked for callbacks"""

    deactivate_on_fail: Annotated[str, PropertyInfo(alias="deactivateOnFail")]
    """A boolean to showing if the transaction should be deactivated on fail or not."""

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """This is the end date of a reccuring transaction"""

    frequency: Literal["on_call", "once", "hourly", "daily", "weekly", "every_[1-366]d"]
    """This is the frequency of a reccuring transaction"""

    retry_frequency: Annotated[Literal["once", "hourly", "daily"], PropertyInfo(alias="retryFrequency")]
    """The retry frequencies"""

    retry_on_fail: Annotated[bool, PropertyInfo(alias="retryOnFail")]
    """A boolean to showing if the transaction should be retried on fail or not."""

    retry_run: Annotated[str, PropertyInfo(alias="retryRun")]
    """This is the retry run"""

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """This is the start date of a reccuring transaction"""

    type: str
    """Type of the invoice being paid for"""


class PaymentMethodDetailsLoyaltyAccount(TypedDict, total=False):
    id: str
    """Unique identifier of the loyalty account."""

    description: str
    """Description of the associated loyalty account."""

    name: str
    """Entity name."""


class PaymentMethodDetailsTokenizedCard(TypedDict, total=False):
    token: str
    """The token itself ie. a token id associated with a the payment card."""

    brand: str
    """Card brand. Might be used for display purposes."""

    issuer: str
    """Whoever issued the token."""

    last_four_digits: Annotated[str, PropertyInfo(alias="lastFourDigits")]
    """Last four digits of the credit card or a token authentication PIN.

    Might be used for display purposes.
    """

    token_type: Annotated[str, PropertyInfo(alias="tokenType")]
    """Token type. e.g emv."""

    type: str
    """Card type. Might be used for display purposes."""


class PaymentMethodDetailsVoucher(TypedDict, total=False):
    campaign: str
    """Campaign this voucher belongs to."""

    code: str
    """Code that identifies the voucher."""

    description: str
    """Description of the voucher. i,e, Get one and receive one free."""

    expiration_date: Annotated[Union[str, datetime], PropertyInfo(alias="expirationDate", format="iso8601")]
    """The vouchers expiration date."""

    value: str
    """Discount that the voucher applies when its a discount voucher."""


class PaymentMethodDetails(TypedDict, total=False):
    account: PaymentMethodDetailsAccount
    """Detailed information for a Telco Account."""

    bank_account_debit: Annotated[PaymentMethodDetailsBankAccountDebit, PropertyInfo(alias="bankAccountDebit")]
    """Detailed information for a bank account debit."""

    bank_account_transfer: Annotated[PaymentMethodDetailsBankAccountTransfer, PropertyInfo(alias="bankAccountTransfer")]
    """Detailed information for a bank account transfer."""

    bank_card: Annotated[PaymentMethodDetailsBankCard, PropertyInfo(alias="bankCard")]
    """Detailed information for a bank card."""

    bucket: PaymentMethodDetailsBucket
    """
    Detailed information for a bucket that could be used to perform the payment,
    especially in the pre-paid environment.
    """

    digital_wallet: Annotated[PaymentMethodDetailsDigitalWallet, PropertyInfo(alias="digitalWallet")]
    """Detailed information for a Digital Wallet."""

    invoice: PaymentMethodDetailsInvoice
    """Detailed information for an invoice"""

    loyalty_account: Annotated[PaymentMethodDetailsLoyaltyAccount, PropertyInfo(alias="loyaltyAccount")]
    """
    Detailed information for a loyalty system that could be used to perform the
    payment..
    """

    tokenized_card: Annotated[PaymentMethodDetailsTokenizedCard, PropertyInfo(alias="tokenizedCard")]
    """Detailed information for a stored tokenized card."""

    voucher: PaymentMethodDetailsVoucher
    """Detailed information for a voucher."""


class PaymentMethod(TypedDict, total=False):
    type: Required[
        Literal[
            "BankCard",
            "TokenizedCard",
            "BankAccountDebit",
            "BankAccountTransfer",
            "Account",
            "LoyaltyAccount",
            "Bucket",
            "Voucher",
            "DigitalWallet",
            "Airtime",
            "Mobile Money",
            "Invoice",
        ]
    ]

    description: str
    """Description of the associated payment method."""

    details: PaymentMethodDetails
    """Definition of the payment method. Its content depends on the type field."""

    name: str
    """Friendly name assigned to the payment method."""

    valid_from: Annotated[Union[str, datetime], PropertyInfo(alias="validFrom", format="iso8601")]
    """Period the payment method is valid."""

    valid_to: Annotated[Union[str, datetime], PropertyInfo(alias="validTo", format="iso8601")]
    """Period the payment method is valid."""


class TotalAmount(TypedDict, total=False):
    amount: Required[float]
    """Amount of money"""

    units: Required[str]
    """Currency"""


class AdditionalInformation(TypedDict, total=False):
    description: Required[str]
    """Description of additional information item."""

    name: Required[str]
    """Name of additional information item."""


class Amount(TypedDict, total=False):
    amount: Required[float]
    """Amount of money"""

    units: Required[str]
    """Currency"""


class PayeeTotalAmount(TypedDict, total=False):
    amount: Required[float]
    """Amount of money"""

    units: Required[str]
    """Currency"""


class PayeeAmount(TypedDict, total=False):
    amount: Required[float]
    """Amount of money"""

    units: Required[str]
    """Currency"""


class PayeeTaxAmount(TypedDict, total=False):
    amount: Required[float]
    """Amount of money"""

    units: Required[str]
    """Currency"""


class Payee(TypedDict, total=False):
    total_amount: Required[Annotated[PayeeTotalAmount, PropertyInfo(alias="totalAmount")]]
    """Representation of monetary value."""

    amount: PayeeAmount
    """Representation of monetary value."""

    payee_id: Annotated[str, PropertyInfo(alias="payeeId")]
    """The Payee identifier, ie. can be a receivingfri or a merchant Id etc."""

    payee_id_type: Annotated[str, PropertyInfo(alias="payeeIdType")]
    """Identifier Type of the Payee."""

    payee_name: Annotated[str, PropertyInfo(alias="payeeName")]
    """Name of the payee"""

    payee_note: Annotated[str, PropertyInfo(alias="payeeNote")]
    """A descriptive note for receiver transaction history, ie. a receiver message"""

    tax_amount: Annotated[PayeeTaxAmount, PropertyInfo(alias="taxAmount")]
    """Representation of monetary value."""


class Payer(TypedDict, total=False):
    payer_id: Required[Annotated[str, PropertyInfo(alias="payerId")]]
    """The Payer identifier, can be a sending fri, an msisdn etc."""

    include_payer_charges: Annotated[bool, PropertyInfo(alias="includePayerCharges")]
    """A boolean value to add payment charges"""

    payer_email: Annotated[str, PropertyInfo(alias="payerEmail")]
    """An optional email address of the payer or customer"""

    payer_id_type: Annotated[str, PropertyInfo(alias="payerIdType")]
    """Identifier Type of the Payer."""

    payer_name: Annotated[str, PropertyInfo(alias="payerName")]
    """Name of the payer"""

    payer_note: Annotated[str, PropertyInfo(alias="payerNote")]
    """A descriptive note for sender transaction history,ex. a sender note"""

    payer_ref: Annotated[str, PropertyInfo(alias="payerRef")]
    """A reference to the payer"""

    payer_surname: Annotated[str, PropertyInfo(alias="payerSurname")]
    """Surname of the payer"""


class TaxAmount(TypedDict, total=False):
    amount: Required[float]
    """Amount of money"""

    units: Required[str]
    """Currency"""
