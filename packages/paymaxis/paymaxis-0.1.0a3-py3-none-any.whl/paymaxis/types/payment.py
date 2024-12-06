# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "Payment",
    "Result",
    "ResultBillingAddress",
    "ResultCustomer",
    "ResultPaymentMethodDetails",
]


class ResultBillingAddress(BaseModel):
    address_line1: Optional[str] = FieldInfo(alias="addressLine1", default=None)
    """Line 1 of the address (e.g., Number, street, etc)"""

    address_line2: Optional[str] = FieldInfo(alias="addressLine2", default=None)
    """Line 2 of the address (e.g., Suite, apt)"""

    city: Optional[str] = None
    """City name"""

    country_code: Optional[str] = FieldInfo(alias="countryCode", default=None)
    """2-character IS0-3166-1 country code"""

    postal_code: Optional[str] = FieldInfo(alias="postalCode", default=None)
    """Postal code"""

    state: Optional[str] = None
    """State code"""


class ResultCustomer(BaseModel):
    account_name: Optional[str] = FieldInfo(alias="accountName", default=None)
    """Customer account name in the provider's system.

    Used for some types of withdrawals.
    """

    account_number: Optional[str] = FieldInfo(alias="accountNumber", default=None)
    """Customer account number in the provider's system.

    Used for some types of withdrawals.
    """

    bank: Optional[str] = None
    """Customer bank. Used for some types of withdrawals."""

    bank_branch: Optional[str] = FieldInfo(alias="bankBranch", default=None)
    """Customer bank branch. Used for some types of withdrawals."""

    citizenship_country_code: Optional[str] = FieldInfo(
        alias="citizenshipCountryCode", default=None
    )
    """Customer country of citizenship"""

    date_of_birth: Optional[str] = FieldInfo(alias="dateOfBirth", default=None)

    date_of_first_deposit: Optional[str] = FieldInfo(
        alias="dateOfFirstDeposit", default=None
    )
    """Date of the first deposit from the customer"""

    deposits_amount: Optional[int] = FieldInfo(alias="depositsAmount", default=None)
    """How much the customer has deposited, in base currency"""

    deposits_cnt: Optional[int] = FieldInfo(alias="depositsCnt", default=None)
    """How many times the customer made a deposit"""

    document_number: Optional[str] = FieldInfo(alias="documentNumber", default=None)
    """An identifier for the customer assigned by a government authority"""

    document_type: Optional[
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
        ]
    ] = FieldInfo(alias="documentType", default=None)
    """Document Type"""

    email: Optional[str] = None
    """Email address of the customer"""

    first_name: Optional[str] = FieldInfo(alias="firstName", default=None)

    kyc_status: Optional[bool] = FieldInfo(alias="kycStatus", default=None)
    """Indicates whether the customer has passed KYC verification"""

    last_name: Optional[str] = FieldInfo(alias="lastName", default=None)

    locale: Optional[str] = None
    """Customer preferred display language"""

    payment_instrument_kyc_status: Optional[bool] = FieldInfo(
        alias="paymentInstrumentKycStatus", default=None
    )
    """
    Indicates whether the payment instrument (usually the card number) has passed
    KYC verification
    """

    phone: Optional[str] = None
    """International phone number of the customer, without the '+'.

    Use a space as a separator between the dialing country code and local phone
    number.
    """

    reference_id: Optional[str] = FieldInfo(alias="referenceId", default=None)
    """Id of the customer assigned by Merchant"""

    routing_group: Optional[str] = FieldInfo(alias="routingGroup", default=None)
    """Identify the customer as belonging to a specific group that is used for routing"""

    withdrawals_amount: Optional[int] = FieldInfo(
        alias="withdrawalsAmount", default=None
    )
    """How much the customer has withdrawn, in base currency"""

    withdrawals_cnt: Optional[int] = FieldInfo(alias="withdrawalsCnt", default=None)
    """How many times the customer made a withdrawal"""


class ResultPaymentMethodDetails(BaseModel):
    card_expiry_month: Optional[str] = FieldInfo(alias="cardExpiryMonth", default=None)
    """Card expiration month (for BASIC_CARD payment method only)"""

    card_expiry_year: Optional[str] = FieldInfo(alias="cardExpiryYear", default=None)
    """Card expiration year (for BASIC_CARD payment method only)"""

    cardholder_name: Optional[str] = FieldInfo(alias="cardholderName", default=None)
    """Cardholder name (for BASIC_CARD payment method only)"""

    card_issuing_country_code: Optional[str] = FieldInfo(
        alias="cardIssuingCountryCode", default=None
    )
    """Card issuing country code (for BASIC_CARD payment method only)"""

    customer_account_number: Optional[str] = FieldInfo(
        alias="customerAccountNumber", default=None
    )
    """Customer account Id in external system or masked card PAN"""


class Result(BaseModel):
    id: Optional[str] = None
    """Payment Id"""

    amount: Optional[float] = None
    """Amount sent to the payment provider"""

    billing_address: Optional[ResultBillingAddress] = FieldInfo(
        alias="billingAddress", default=None
    )
    """Customer's billing address"""

    currency: Optional[str] = None
    """Currency sent to the payment provider"""

    customer: Optional[ResultCustomer] = None

    customer_amount: Optional[float] = FieldInfo(alias="customerAmount", default=None)
    """Amount from payment request.

    Filled only if the request currency differs from the currency sent to the
    payment provider.
    """

    customer_currency: Optional[str] = FieldInfo(alias="customerCurrency", default=None)
    """Currency from payment request.

    Filled only if it differs from the currency sent to the payment provider.
    """

    description: Optional[str] = None
    """Description of the transaction"""

    error_code: Optional[str] = FieldInfo(alias="errorCode", default=None)
    """Check 'Error Codes' section for details"""

    external_fee_amount: Optional[float] = FieldInfo(
        alias="externalFeeAmount", default=None
    )
    """Provider fee. Filled only if supported by the provider."""

    external_fee_currency: Optional[str] = FieldInfo(
        alias="externalFeeCurrency", default=None
    )
    """Provider fee currency. Filled only if supported by the provider."""

    external_result_code: Optional[str] = FieldInfo(
        alias="externalResultCode", default=None
    )
    """Result code from external provider"""

    parent_payment_id: Optional[str] = FieldInfo(alias="parentPaymentId", default=None)
    """Initial transaction Id from payment request"""

    payment_method: Optional[
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
        ]
    ] = FieldInfo(alias="paymentMethod", default=None)
    """Payment Method"""

    payment_method_details: Optional[ResultPaymentMethodDetails] = FieldInfo(
        alias="paymentMethodDetails", default=None
    )

    payment_type: Optional[Literal["DEPOSIT", "WITHDRAWAL", "REFUND"]] = FieldInfo(
        alias="paymentType", default=None
    )
    """Payment Type"""

    recurring_token: Optional[str] = FieldInfo(alias="recurringToken", default=None)
    """Token that can be used to continue the recurring chain"""

    redirect_url: Optional[str] = FieldInfo(alias="redirectUrl", default=None)
    """URL to redirect the customer"""

    reference_id: Optional[str] = FieldInfo(alias="referenceId", default=None)
    """referenceId from payment request"""

    start_recurring: Optional[bool] = FieldInfo(alias="startRecurring", default=None)
    """Indicates whether this payment has started a recurring chain"""

    state: Optional[
        Literal["CHECKOUT", "PENDING", "CANCELLED", "DECLINED", "COMPLETED"]
    ] = None
    """Payment State"""

    terminal_name: Optional[str] = FieldInfo(alias="terminalName", default=None)
    """The name of the provider that was used to process this payment"""


class Payment(BaseModel):
    result: Optional[Result] = None

    status: Optional[int] = None
    """HTTP status code"""

    timestamp: Optional[str] = None
