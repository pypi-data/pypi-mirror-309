# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from paymaxis import Paymaxis, AsyncPaymaxis
from tests.utils import assert_matches_type
from paymaxis.types import Subscription

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubscriptions:
    parametrize = pytest.mark.parametrize(
        "client", [False, True], indirect=True, ids=["loose", "strict"]
    )

    @parametrize
    def test_method_retrieve(self, client: Paymaxis) -> None:
        subscription = client.subscriptions.retrieve(
            "id",
        )
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Paymaxis) -> None:
        response = client.subscriptions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Paymaxis) -> None:
        with client.subscriptions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(Subscription, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Paymaxis) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `id` but received ''"
        ):
            client.subscriptions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Paymaxis) -> None:
        subscription = client.subscriptions.update(
            id="id",
        )
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Paymaxis) -> None:
        subscription = client.subscriptions.update(
            id="id",
            state="CANCELLED",
        )
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Paymaxis) -> None:
        response = client.subscriptions.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Paymaxis) -> None:
        with client.subscriptions.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(Subscription, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Paymaxis) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `id` but received ''"
        ):
            client.subscriptions.with_raw_response.update(
                id="",
            )


class TestAsyncSubscriptions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True], indirect=True, ids=["loose", "strict"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPaymaxis) -> None:
        subscription = await async_client.subscriptions.retrieve(
            "id",
        )
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPaymaxis) -> None:
        response = await async_client.subscriptions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(
        self, async_client: AsyncPaymaxis
    ) -> None:
        async with async_client.subscriptions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(Subscription, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPaymaxis) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `id` but received ''"
        ):
            await async_client.subscriptions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncPaymaxis) -> None:
        subscription = await async_client.subscriptions.update(
            id="id",
        )
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(
        self, async_client: AsyncPaymaxis
    ) -> None:
        subscription = await async_client.subscriptions.update(
            id="id",
            state="CANCELLED",
        )
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPaymaxis) -> None:
        response = await async_client.subscriptions.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(Subscription, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPaymaxis) -> None:
        async with async_client.subscriptions.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(Subscription, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncPaymaxis) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `id` but received ''"
        ):
            await async_client.subscriptions.with_raw_response.update(
                id="",
            )
