# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal

import httpx

from ...types import payment_list_params, payment_create_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .operations import (
    OperationsResource,
    AsyncOperationsResource,
    OperationsResourceWithRawResponse,
    AsyncOperationsResourceWithRawResponse,
    OperationsResourceWithStreamingResponse,
    AsyncOperationsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.payment import Payment
from ...types.payment_list_response import PaymentListResponse

__all__ = ["PaymentsResource", "AsyncPaymentsResource"]


class PaymentsResource(SyncAPIResource):
    @cached_property
    def operations(self) -> OperationsResource:
        return OperationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> PaymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/paymaxis-python#accessing-raw-response-data-eg-headers
        """
        return PaymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PaymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/paymaxis-python#with_streaming_response
        """
        return PaymentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        currency: str,
        payment_type: Literal["DEPOSIT", "WITHDRAWAL", "REFUND"],
        additional_parameters: Dict[str, str] | NotGiven = NOT_GIVEN,
        amount: float | NotGiven = NOT_GIVEN,
        billing_address: payment_create_params.BillingAddress | NotGiven = NOT_GIVEN,
        card: payment_create_params.Card | NotGiven = NOT_GIVEN,
        customer: payment_create_params.Customer | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        parent_payment_id: str | NotGiven = NOT_GIVEN,
        payment_method: (
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
            | NotGiven
        ) = NOT_GIVEN,
        recurring_token: str | NotGiven = NOT_GIVEN,
        reference_id: str | NotGiven = NOT_GIVEN,
        return_url: str | NotGiven = NOT_GIVEN,
        start_recurring: bool | NotGiven = NOT_GIVEN,
        subscription: payment_create_params.Subscription | NotGiven = NOT_GIVEN,
        webhook_url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Payment:
        """
        Payment request, used for DEPOSITS, WITHDRAWALS and REFUNDS

        Args:
          currency: Payment currency

          payment_type: Payment Type

          additional_parameters: Additional parameters required by some payment providers. Contact support for
              more information.

          amount: Payment amount

          billing_address: Customer's billing address

          card: You must be PCI DSS compliant to collect card data on your side. If you are not
              certified, do not add this field to your request and we will collect the data on
              our page.

          description: Description of the transaction shown to the Customer. Can be sent outside the
              system.

          parent_payment_id: Id of initial deposit for refunds, Id of initial recurring payment for
              subsequent payments

          payment_method: Payment Method

          recurring_token: To continue recurring chain, send a token from a previously initiated recurring
              payment.

          reference_id: Reference assigned by Merchant. Will not go outside the system. Will be sent
              unchanged in the PaymentResponse.

          return_url: URL to redirect Customer after processing

          start_recurring: Send 'true' if you want this payment to initiate recurring chain. Default is
              'false'.

          subscription: Subscription to bill customers at regular intervals. Used only with
              'startRecurring=true'.

          webhook_url: Url to receive payment status notifications

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/payments",
            body=maybe_transform(
                {
                    "currency": currency,
                    "payment_type": payment_type,
                    "additional_parameters": additional_parameters,
                    "amount": amount,
                    "billing_address": billing_address,
                    "card": card,
                    "customer": customer,
                    "description": description,
                    "parent_payment_id": parent_payment_id,
                    "payment_method": payment_method,
                    "recurring_token": recurring_token,
                    "reference_id": reference_id,
                    "return_url": return_url,
                    "start_recurring": start_recurring,
                    "subscription": subscription,
                    "webhook_url": webhook_url,
                },
                payment_create_params.PaymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Payment,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Payment:
        """
        Find Payment by Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/api/v1/payments/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Payment,
        )

    def list(
        self,
        *,
        created: payment_list_params.Created | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        updated: payment_list_params.Updated | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentListResponse:
        """
        Get a list of payments sorted by creation date (most recent first)

        Args:
          limit: The numbers of items to return. Default is 50.

          offset: The number of items to skip before starting to collect the result set. Default
              is 0.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v1/payments",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created": created,
                        "limit": limit,
                        "offset": offset,
                        "updated": updated,
                    },
                    payment_list_params.PaymentListParams,
                ),
            ),
            cast_to=PaymentListResponse,
        )


class AsyncPaymentsResource(AsyncAPIResource):
    @cached_property
    def operations(self) -> AsyncOperationsResource:
        return AsyncOperationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPaymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TralahM/paymaxis-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPaymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPaymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TralahM/paymaxis-python#with_streaming_response
        """
        return AsyncPaymentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        currency: str,
        payment_type: Literal["DEPOSIT", "WITHDRAWAL", "REFUND"],
        additional_parameters: Dict[str, str] | NotGiven = NOT_GIVEN,
        amount: float | NotGiven = NOT_GIVEN,
        billing_address: payment_create_params.BillingAddress | NotGiven = NOT_GIVEN,
        card: payment_create_params.Card | NotGiven = NOT_GIVEN,
        customer: payment_create_params.Customer | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        parent_payment_id: str | NotGiven = NOT_GIVEN,
        payment_method: (
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
            | NotGiven
        ) = NOT_GIVEN,
        recurring_token: str | NotGiven = NOT_GIVEN,
        reference_id: str | NotGiven = NOT_GIVEN,
        return_url: str | NotGiven = NOT_GIVEN,
        start_recurring: bool | NotGiven = NOT_GIVEN,
        subscription: payment_create_params.Subscription | NotGiven = NOT_GIVEN,
        webhook_url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Payment:
        """
        Payment request, used for DEPOSITS, WITHDRAWALS and REFUNDS

        Args:
          currency: Payment currency

          payment_type: Payment Type

          additional_parameters: Additional parameters required by some payment providers. Contact support for
              more information.

          amount: Payment amount

          billing_address: Customer's billing address

          card: You must be PCI DSS compliant to collect card data on your side. If you are not
              certified, do not add this field to your request and we will collect the data on
              our page.

          description: Description of the transaction shown to the Customer. Can be sent outside the
              system.

          parent_payment_id: Id of initial deposit for refunds, Id of initial recurring payment for
              subsequent payments

          payment_method: Payment Method

          recurring_token: To continue recurring chain, send a token from a previously initiated recurring
              payment.

          reference_id: Reference assigned by Merchant. Will not go outside the system. Will be sent
              unchanged in the PaymentResponse.

          return_url: URL to redirect Customer after processing

          start_recurring: Send 'true' if you want this payment to initiate recurring chain. Default is
              'false'.

          subscription: Subscription to bill customers at regular intervals. Used only with
              'startRecurring=true'.

          webhook_url: Url to receive payment status notifications

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/payments",
            body=await async_maybe_transform(
                {
                    "currency": currency,
                    "payment_type": payment_type,
                    "additional_parameters": additional_parameters,
                    "amount": amount,
                    "billing_address": billing_address,
                    "card": card,
                    "customer": customer,
                    "description": description,
                    "parent_payment_id": parent_payment_id,
                    "payment_method": payment_method,
                    "recurring_token": recurring_token,
                    "reference_id": reference_id,
                    "return_url": return_url,
                    "start_recurring": start_recurring,
                    "subscription": subscription,
                    "webhook_url": webhook_url,
                },
                payment_create_params.PaymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Payment,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Payment:
        """
        Find Payment by Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/api/v1/payments/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Payment,
        )

    async def list(
        self,
        *,
        created: payment_list_params.Created | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        updated: payment_list_params.Updated | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PaymentListResponse:
        """
        Get a list of payments sorted by creation date (most recent first)

        Args:
          limit: The numbers of items to return. Default is 50.

          offset: The number of items to skip before starting to collect the result set. Default
              is 0.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v1/payments",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "created": created,
                        "limit": limit,
                        "offset": offset,
                        "updated": updated,
                    },
                    payment_list_params.PaymentListParams,
                ),
            ),
            cast_to=PaymentListResponse,
        )


class PaymentsResourceWithRawResponse:
    def __init__(self, payments: PaymentsResource) -> None:
        self._payments = payments

        self.create = to_raw_response_wrapper(
            payments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            payments.retrieve,
        )
        self.list = to_raw_response_wrapper(
            payments.list,
        )

    @cached_property
    def operations(self) -> OperationsResourceWithRawResponse:
        return OperationsResourceWithRawResponse(self._payments.operations)


class AsyncPaymentsResourceWithRawResponse:
    def __init__(self, payments: AsyncPaymentsResource) -> None:
        self._payments = payments

        self.create = async_to_raw_response_wrapper(
            payments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            payments.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            payments.list,
        )

    @cached_property
    def operations(self) -> AsyncOperationsResourceWithRawResponse:
        return AsyncOperationsResourceWithRawResponse(self._payments.operations)


class PaymentsResourceWithStreamingResponse:
    def __init__(self, payments: PaymentsResource) -> None:
        self._payments = payments

        self.create = to_streamed_response_wrapper(
            payments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            payments.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            payments.list,
        )

    @cached_property
    def operations(self) -> OperationsResourceWithStreamingResponse:
        return OperationsResourceWithStreamingResponse(self._payments.operations)


class AsyncPaymentsResourceWithStreamingResponse:
    def __init__(self, payments: AsyncPaymentsResource) -> None:
        self._payments = payments

        self.create = async_to_streamed_response_wrapper(
            payments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            payments.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            payments.list,
        )

    @cached_property
    def operations(self) -> AsyncOperationsResourceWithStreamingResponse:
        return AsyncOperationsResourceWithStreamingResponse(self._payments.operations)
