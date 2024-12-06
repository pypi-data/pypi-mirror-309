# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "PaymentCreateParams",
    "BillingAddress",
    "Card",
    "Customer",
    "Subscription",
    "SubscriptionRetryStrategy",
]


class PaymentCreateParams(TypedDict, total=False):
    currency: Required[str]
    """Payment currency"""

    payment_type: Required[
        Annotated[
            Literal["DEPOSIT", "WITHDRAWAL", "REFUND"],
            PropertyInfo(alias="paymentType"),
        ]
    ]
    """Payment Type"""

    additional_parameters: Annotated[
        Dict[str, str], PropertyInfo(alias="additionalParameters")
    ]
    """Additional parameters required by some payment providers.

    Contact support for more information.
    """

    amount: float
    """Payment amount"""

    billing_address: Annotated[BillingAddress, PropertyInfo(alias="billingAddress")]
    """Customer's billing address"""

    card: Card
    """You must be PCI DSS compliant to collect card data on your side.

    If you are not certified, do not add this field to your request and we will
    collect the data on our page.
    """

    customer: Customer

    description: str
    """Description of the transaction shown to the Customer.

    Can be sent outside the system.
    """

    parent_payment_id: Annotated[str, PropertyInfo(alias="parentPaymentId")]
    """
    Id of initial deposit for refunds, Id of initial recurring payment for
    subsequent payments
    """

    payment_method: Annotated[
        Literal[
            "BASIC_CARD",
            "CRYPTO",
            "FLEXEPIN",
            "MACROPAY",
            "SKRILL",
            "PAYRETAILERS",
            "LOCALPAYMENT",
            "MONNET",
            "PAYPAL",
            "NETELLER",
            "TRUSTPAYMENTS",
            "PAYMAXIS",
            "GATE8TRANSACT",
            "TINK",
            "B2BINPAY",
            "CLICK",
            "MONETIX",
            "PERFECTMONEY",
            "VOLT",
            "KESSPAY",
            "BILLLINE",
            "NGENIUS",
            "ASTROPAY",
            "ALYCEPAY",
            "PIX",
            "BOLETO",
            "UPI",
            "PAYTM",
            "NETBANKING",
            "FINRAX",
            "SPOYNT",
            "XINPAY",
            "OMNIMATRIX",
            "DPOPAY",
            "EXTERNAL_HPP",
            "XANPAY",
            "INRPAY",
            "ARI10",
            "SOFORT",
            "GIROPAY",
            "PAYSAFECARD",
            "PAYSAFECASH",
            "OPEN_BANKING",
            "KLARNA",
            "SPEI",
            "PAYCASH",
            "RAPIPAGO",
            "PAGOFACIL",
            "RAPIDTRANSFER",
            "MOBILE_MONEY",
            "INTERAC",
            "INTERAC_ETO",
            "INTERAC_RTO",
            "INTERAC_ACH",
            "PICPAY",
            "MOLLIE",
            "TED",
            "ZIPAY",
            "PSE",
            "EFECTY",
            "BANKTRANSFER",
            "PEC",
            "OXXO",
            "WEBPAY",
            "PAGOEFECTIVO",
            "MIFINITY",
            "PAYPORT",
            "JETONCASH",
            "JETONWALLET",
            "NODA",
            "NODA_REVOLUT",
            "ALFAKIT",
            "PAYFUN",
            "EMANAT",
            "M10",
            "RUBPAY",
            "MONERCHY",
            "MUCHBETTER",
            "YAPILY",
            "INAI",
            "IMPS",
            "RTGS",
            "PAYID",
            "ZOTAPAY",
            "SBP",
            "P2P_CARD",
            "P2P_IBAN",
            "P2P_SBP",
            "P2P_MOBILE",
            "PUSH",
            "GATEIQ",
            "VIETTEL",
            "ZALO",
            "QR",
            "CUP",
            "CODI",
            "PAY2PLAY",
            "BKASH",
            "NAGAD",
            "ROCKET",
            "VIRTUAL_ACCOUNT",
            "MULTIBANCO",
            "BLIK",
            "MBWAY",
            "P24",
            "MISTERCASH",
            "MACH",
            "KHIPU",
            "NEFT",
            "STICPAY",
            "SBERPAY",
            "MOBILE_COMMERCE",
            "BINANCE_PAY",
            "MPAY",
            "CHEK",
            "KLAP_EFECTIVO",
            "KLAP_TRANSFERENCIA",
            "PAGO46",
            "HITES",
            "SERVIFACIL",
            "OPENPAYD",
            "FAWRY",
            "EPS",
            "IDEAL",
            "TRUSTLY",
            "USSD",
            "MPESA",
            "ENAIRA",
            "ONEVOUCHER",
            "BANCONTACT",
            "SWISH",
            "EFT",
            "GCASH",
            "PAYMAYA",
            "PAGO_MOVIL",
            "PAGO_MOVIL_INST",
            "BIOPAGO",
            "CASH",
            "VOUCHERRY",
            "APPLEPAY",
            "GOOGLEPAY",
            "BRITE",
            "VOUCHSTAR",
            "REVOLUT",
            "ONLINE_BANKING",
            "PROMPTPAY",
            "TRUEMONEY",
            "MOMOPAY_VN",
            "MOMOPAY_RW",
            "VNPAY_QR",
            "N26",
            "WISE",
            "PAYDO_WALLET",
            "PAPARA",
            "PAYOUT_SEPA_BATCH",
            "PAYOUT_NONSEPA_REQUEST",
        ],
        PropertyInfo(alias="paymentMethod"),
    ]
    """Payment Method"""

    recurring_token: Annotated[str, PropertyInfo(alias="recurringToken")]
    """
    To continue recurring chain, send a token from a previously initiated recurring
    payment.
    """

    reference_id: Annotated[str, PropertyInfo(alias="referenceId")]
    """Reference assigned by Merchant.

    Will not go outside the system. Will be sent unchanged in the PaymentResponse.
    """

    return_url: Annotated[str, PropertyInfo(alias="returnUrl")]
    """URL to redirect Customer after processing"""

    start_recurring: Annotated[bool, PropertyInfo(alias="startRecurring")]
    """Send 'true' if you want this payment to initiate recurring chain.

    Default is 'false'.
    """

    subscription: Subscription
    """Subscription to bill customers at regular intervals.

    Used only with 'startRecurring=true'.
    """

    webhook_url: Annotated[str, PropertyInfo(alias="webhookUrl")]
    """Url to receive payment status notifications"""


class BillingAddress(TypedDict, total=False):
    address_line1: Annotated[str, PropertyInfo(alias="addressLine1")]
    """Line 1 of the address (e.g., Number, street, etc)"""

    address_line2: Annotated[str, PropertyInfo(alias="addressLine2")]
    """Line 2 of the address (e.g., Suite, apt)"""

    city: str
    """City name"""

    country_code: Annotated[str, PropertyInfo(alias="countryCode")]
    """2-character IS0-3166-1 country code"""

    postal_code: Annotated[str, PropertyInfo(alias="postalCode")]
    """Postal code"""

    state: str
    """State code"""


class Card(TypedDict, total=False):
    cardholder_name: Annotated[str, PropertyInfo(alias="cardholderName")]
    """Cardholder's name printed on the card"""

    card_number: Annotated[str, PropertyInfo(alias="cardNumber")]
    """Card primary account number (PAN). All non-numeric characters will be ignored."""

    card_security_code: Annotated[str, PropertyInfo(alias="cardSecurityCode")]
    """Card security code (CVV2 / CVC2 / CAV2)"""

    expiry_month: Annotated[str, PropertyInfo(alias="expiryMonth")]
    """Card expiration month, 2 digits"""

    expiry_year: Annotated[str, PropertyInfo(alias="expiryYear")]
    """Card expiration year, 4 digits"""


class Customer(TypedDict, total=False):
    account_name: Annotated[str, PropertyInfo(alias="accountName")]
    """Customer account name in the provider's system.

    Used for some types of withdrawals.
    """

    account_number: Annotated[str, PropertyInfo(alias="accountNumber")]
    """Customer account number in the provider's system.

    Used for some types of withdrawals.
    """

    bank: str
    """Customer bank. Used for some types of withdrawals."""

    bank_branch: Annotated[str, PropertyInfo(alias="bankBranch")]
    """Customer bank branch. Used for some types of withdrawals."""

    citizenship_country_code: Annotated[
        str, PropertyInfo(alias="citizenshipCountryCode")
    ]
    """Customer country of citizenship"""

    date_of_birth: Annotated[str, PropertyInfo(alias="dateOfBirth")]

    date_of_first_deposit: Annotated[str, PropertyInfo(alias="dateOfFirstDeposit")]
    """Date of the first deposit from the customer"""

    deposits_amount: Annotated[int, PropertyInfo(alias="depositsAmount")]
    """How much the customer has deposited, in base currency"""

    deposits_cnt: Annotated[int, PropertyInfo(alias="depositsCnt")]
    """How many times the customer made a deposit"""

    document_number: Annotated[str, PropertyInfo(alias="documentNumber")]
    """An identifier for the customer assigned by a government authority"""

    document_type: Annotated[
        Literal[
            "AR_CDI",
            "AR_CUIL",
            "AR_CUIT",
            "AR_DNI",
            "AR_OTRO",
            "BR_CNPJ",
            "BR_CPF",
            "CL_OTRO",
            "CL_RUN",
            "CL_RUT",
            "CO_CC",
            "CO_CE",
            "CO_DL",
            "CO_DNI",
            "CO_NE",
            "CO_NIT",
            "CO_PP",
            "CO_SS",
            "CO_TI",
            "CR_CDI",
            "EC_DNI",
            "EC_PP",
            "EC_RUC",
            "GT_CUI",
            "GT_DPI",
            "GT_NIT",
            "MX_CURP",
            "MX_IFE",
            "MX_PP",
            "MX_RFC",
            "PA_CIP",
            "PE_CE",
            "PE_DNI",
            "PE_OTRO",
            "PE_PP",
            "PE_RUC",
        ],
        PropertyInfo(alias="documentType"),
    ]
    """Document Type"""

    email: str
    """Email address of the customer"""

    first_name: Annotated[str, PropertyInfo(alias="firstName")]

    kyc_status: Annotated[bool, PropertyInfo(alias="kycStatus")]
    """Indicates whether the customer has passed KYC verification"""

    last_name: Annotated[str, PropertyInfo(alias="lastName")]

    locale: str
    """Customer preferred display language"""

    payment_instrument_kyc_status: Annotated[
        bool, PropertyInfo(alias="paymentInstrumentKycStatus")
    ]
    """
    Indicates whether the payment instrument (usually the card number) has passed
    KYC verification
    """

    phone: str
    """International phone number of the customer, without the '+'.

    Use a space as a separator between the dialing country code and local phone
    number.
    """

    reference_id: Annotated[str, PropertyInfo(alias="referenceId")]
    """Id of the customer assigned by Merchant"""

    routing_group: Annotated[str, PropertyInfo(alias="routingGroup")]
    """Identify the customer as belonging to a specific group that is used for routing"""

    withdrawals_amount: Annotated[int, PropertyInfo(alias="withdrawalsAmount")]
    """How much the customer has withdrawn, in base currency"""

    withdrawals_cnt: Annotated[int, PropertyInfo(alias="withdrawalsCnt")]
    """How many times the customer made a withdrawal"""


class SubscriptionRetryStrategy(TypedDict, total=False):
    frequency: Required[int]
    """
    The number of intervals after which the system will retry the payment after an
    unsuccessful attempt
    """

    number_of_cycles: Required[Annotated[int, PropertyInfo(alias="numberOfCycles")]]
    """Required number of retries"""

    amount_adjustments: Annotated[
        Iterable[int], PropertyInfo(alias="amountAdjustments")
    ]
    """
    If specified, the nth element contains the percentage of the initial amount that
    will be charged for the nth retry
    """

    frequency_unit: Annotated[
        Literal["MINUTE", "DAY", "WEEK", "MONTH"], PropertyInfo(alias="frequencyUnit")
    ]
    """The interval at which the subscription is retried.

    Use 'MINUTE' for testing purposes only.
    """


class Subscription(TypedDict, total=False):
    frequency: Required[int]
    """The number of intervals after which a subscriber is billed.

    For example, if the frequencyUnit is DAY with an frequency of 2, the
    subscription is billed once every two days.
    """

    amount: float
    """The amount to be used for subsequent payments.

    If not specified, the amount of the original payment is used.
    """

    description: str
    """Description for subsequent recurring payments"""

    frequency_unit: Annotated[
        Literal["MINUTE", "DAY", "WEEK", "MONTH"], PropertyInfo(alias="frequencyUnit")
    ]
    """The interval at which the subscription is billed.

    Use 'MINUTE' for testing purposes only.
    """

    number_of_cycles: Annotated[int, PropertyInfo(alias="numberOfCycles")]
    """Required number of subsequent recurring payments.

    Unlimited if value is not specified.
    """

    retry_strategy: Annotated[
        SubscriptionRetryStrategy, PropertyInfo(alias="retryStrategy")
    ]
    """Retry strategy for subscription.

    If not specified, the subscription is canceled after the first failed payment
    attempt.
    """

    start_time: Annotated[str, PropertyInfo(alias="startTime")]
    """Date and time of the 1st cycle.

    if not specified, then calculated as (initialDeposit.createTime +
    frequency\\**frequencyUnit).
    """
