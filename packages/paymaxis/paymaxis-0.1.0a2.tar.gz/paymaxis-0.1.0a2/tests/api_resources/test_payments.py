# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from paymaxis import Paymaxis, AsyncPaymaxis
from tests.utils import assert_matches_type
from paymaxis.types import Payment, PaymentListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPayments:
    parametrize = pytest.mark.parametrize(
        "client", [False, True], indirect=True, ids=["loose", "strict"]
    )

    @parametrize
    def test_method_create(self, client: Paymaxis) -> None:
        payment = client.payments.create(
            currency="EUR",
            payment_type="DEPOSIT",
        )
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Paymaxis) -> None:
        payment = client.payments.create(
            currency="EUR",
            payment_type="DEPOSIT",
            additional_parameters={
                "bankCode": "ABHY0065032",
                "countryOfBirth": "CY",
            },
            amount=1e-18,
            billing_address={
                "address_line1": "7, Sunny street",
                "address_line2": "Office 3",
                "city": "Limassol",
                "country_code": "CY",
                "postal_code": "4141",
                "state": "CA",
            },
            card={
                "cardholder_name": "John Smith",
                "card_number": "4000 0000 0000 0002",
                "card_security_code": "010",
                "expiry_month": "01",
                "expiry_year": "2030",
            },
            customer={
                "account_name": "accountName",
                "account_number": "accountNumber",
                "bank": "bank",
                "bank_branch": "bankBranch",
                "citizenship_country_code": "AU",
                "date_of_birth": "2001-12-03",
                "date_of_first_deposit": "2021-01-01",
                "deposits_amount": 5000,
                "deposits_cnt": 5000,
                "document_number": "documentNumber",
                "document_type": "AR_CDI",
                "email": "my@email.com",
                "first_name": "John",
                "kyc_status": True,
                "last_name": "Smith",
                "locale": "ru",
                "payment_instrument_kyc_status": True,
                "phone": "357 123123123",
                "reference_id": "customer_123",
                "routing_group": "VIP",
                "withdrawals_amount": 1000,
                "withdrawals_cnt": 1000,
            },
            description="Deposit 123 via TEST shop",
            parent_payment_id="91d27876e87f4b22b3ecd53924bf973d",
            payment_method="BASIC_CARD",
            recurring_token="recurringToken",
            reference_id="payment_id=123;custom_ref=456",
            return_url="https://mywebsite.com/{id}/{referenceId}/{state}/{type}",
            start_recurring=True,
            subscription={
                "frequency": 2,
                "amount": 99.99,
                "description": "Subscription to service",
                "frequency_unit": "MINUTE",
                "number_of_cycles": 12,
                "retry_strategy": {
                    "frequency": 2,
                    "number_of_cycles": 12,
                    "amount_adjustments": [1, 1, 1],
                    "frequency_unit": "MINUTE",
                },
                "start_time": "2030-12-25T10:11:12",
            },
            webhook_url="https://mywebsite.com/webhooks",
        )
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Paymaxis) -> None:
        response = client.payments.with_raw_response.create(
            currency="EUR",
            payment_type="DEPOSIT",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Paymaxis) -> None:
        with client.payments.with_streaming_response.create(
            currency="EUR",
            payment_type="DEPOSIT",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(Payment, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Paymaxis) -> None:
        payment = client.payments.retrieve(
            "id" * 16,
        )
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Paymaxis) -> None:
        response = client.payments.with_raw_response.retrieve(
            "id" * 16,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Paymaxis) -> None:
        with client.payments.with_streaming_response.retrieve(
            "id" * 16,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(Payment, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Paymaxis) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `id` but received ''"
        ):
            client.payments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Paymaxis) -> None:
        payment = client.payments.list()
        assert_matches_type(PaymentListResponse, payment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Paymaxis) -> None:
        payment = client.payments.list(
            created={
                "gte": "2021-10-13T10:26:18",
                "lt": "2021-10-13T10:39:34",
            },
            limit=1,
            offset=0,
            updated={
                "gte": "2021-10-13T10:26:18",
                "lt": "2021-10-13T10:39:34",
            },
        )
        assert_matches_type(PaymentListResponse, payment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Paymaxis) -> None:
        response = client.payments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(PaymentListResponse, payment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Paymaxis) -> None:
        with client.payments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(PaymentListResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPayments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True], indirect=True, ids=["loose", "strict"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncPaymaxis) -> None:
        payment = await async_client.payments.create(
            currency="EUR",
            payment_type="DEPOSIT",
        )
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(
        self, async_client: AsyncPaymaxis
    ) -> None:
        payment = await async_client.payments.create(
            currency="EUR",
            payment_type="DEPOSIT",
            additional_parameters={
                "bankCode": "ABHY0065032",
                "countryOfBirth": "CY",
            },
            amount=1e-18,
            billing_address={
                "address_line1": "7, Sunny street",
                "address_line2": "Office 3",
                "city": "Limassol",
                "country_code": "CY",
                "postal_code": "4141",
                "state": "CA",
            },
            card={
                "cardholder_name": "John Smith",
                "card_number": "4000 0000 0000 0002",
                "card_security_code": "010",
                "expiry_month": "01",
                "expiry_year": "2030",
            },
            customer={
                "account_name": "accountName",
                "account_number": "accountNumber",
                "bank": "bank",
                "bank_branch": "bankBranch",
                "citizenship_country_code": "AU",
                "date_of_birth": "2001-12-03",
                "date_of_first_deposit": "2021-01-01",
                "deposits_amount": 5000,
                "deposits_cnt": 5000,
                "document_number": "documentNumber",
                "document_type": "AR_CDI",
                "email": "my@email.com",
                "first_name": "John",
                "kyc_status": True,
                "last_name": "Smith",
                "locale": "ru",
                "payment_instrument_kyc_status": True,
                "phone": "357 123123123",
                "reference_id": "customer_123",
                "routing_group": "VIP",
                "withdrawals_amount": 1000,
                "withdrawals_cnt": 1000,
            },
            description="Deposit 123 via TEST shop",
            parent_payment_id="91d27876e87f4b22b3ecd53924bf973d",
            payment_method="BASIC_CARD",
            recurring_token="recurringToken",
            reference_id="payment_id=123;custom_ref=456",
            return_url="https://mywebsite.com/{id}/{referenceId}/{state}/{type}",
            start_recurring=True,
            subscription={
                "frequency": 2,
                "amount": 99.99,
                "description": "Subscription to service",
                "frequency_unit": "MINUTE",
                "number_of_cycles": 12,
                "retry_strategy": {
                    "frequency": 2,
                    "number_of_cycles": 12,
                    "amount_adjustments": [1, 1, 1],
                    "frequency_unit": "MINUTE",
                },
                "start_time": "2030-12-25T10:11:12",
            },
            webhook_url="https://mywebsite.com/webhooks",
        )
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPaymaxis) -> None:
        response = await async_client.payments.with_raw_response.create(
            currency="EUR",
            payment_type="DEPOSIT",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPaymaxis) -> None:
        async with async_client.payments.with_streaming_response.create(
            currency="EUR",
            payment_type="DEPOSIT",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(Payment, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPaymaxis) -> None:
        payment = await async_client.payments.retrieve(
            "id" * 16,
        )
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPaymaxis) -> None:
        response = await async_client.payments.with_raw_response.retrieve(
            "id" * 16,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(Payment, payment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(
        self, async_client: AsyncPaymaxis
    ) -> None:
        async with async_client.payments.with_streaming_response.retrieve(
            "id" * 16,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(Payment, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPaymaxis) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `id` but received ''"
        ):
            await async_client.payments.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPaymaxis) -> None:
        payment = await async_client.payments.list()
        assert_matches_type(PaymentListResponse, payment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(
        self, async_client: AsyncPaymaxis
    ) -> None:
        payment = await async_client.payments.list(
            created={
                "gte": "2021-10-13T10:26:18",
                "lt": "2021-10-13T10:39:34",
            },
            limit=1,
            offset=0,
            updated={
                "gte": "2021-10-13T10:26:18",
                "lt": "2021-10-13T10:39:34",
            },
        )
        assert_matches_type(PaymentListResponse, payment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPaymaxis) -> None:
        response = await async_client.payments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(PaymentListResponse, payment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPaymaxis) -> None:
        async with async_client.payments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(PaymentListResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True
