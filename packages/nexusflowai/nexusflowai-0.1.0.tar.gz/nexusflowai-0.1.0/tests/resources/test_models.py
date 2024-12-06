from os import environ

from openai.types import Model
from openai._types import NOT_GIVEN, NotGiven
from openai._models import (
    FinalRequestOptions,
)
from openai.pagination import SyncPage, AsyncPage
from nexusflowai import NexusflowAI, AsyncNexusflowAI
from tests.utils import BASE_URL, API_KEY, MODEL_ID

import pytest
from pytest import fixture

from unittest.mock import MagicMock


def _mock_models_data() -> Model:
    return [
        Model(
            id=MODEL_ID,
            created=1698785189,
            object="model",
            owned_by="nexusflow",
        ),
        Model(
            id=MODEL_ID,
            created=1698785190,
            object="model",
            owned_by="nexusflow",
        ),
    ]


def _final_request_opts() -> None:
    return FinalRequestOptions.construct(
        method="get",
        url="/models",
        params={},
        headers=NOT_GIVEN,
        max_retries=NOT_GIVEN,
        timeout=NOT_GIVEN,
        files=None,
        idempotency_key=None,
        post_parser=None,
        json_data=None,
        extra_json=None,
    )


class TestModels:
    @fixture
    def setup_client(self) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = NexusflowAI(base_url=BASE_URL)

    def test_models(self, setup_client, monkeypatch):
        client = self.client
        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "_request_api_list", post_mock)
        post_mock.return_value = _mock_models_data()

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

        res = client.models.list()
        assert res[0].__class__ == Model
        assert len(res) == 2

        post_mock.assert_called_once_with(Model, SyncPage[Model], _final_request_opts())


class TestAsyncCompletions:
    @fixture
    def setup_client(self) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = AsyncNexusflowAI(base_url=BASE_URL)

    @pytest.mark.asyncio
    async def test_models(self, setup_client, monkeypatch):
        pass
        client = self.client

        post_mock = MagicMock()
        monkeypatch.setattr(AsyncNexusflowAI, "_request_api_list", post_mock)

        async def async_mock_response():
            return _mock_models_data()

        post_mock.return_value = async_mock_response()

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

        res = await client.models.list()
        assert res[0].__class__ == Model
        assert len(res) == 2

        post_mock.assert_called_once_with(
            Model, AsyncPage[Model], _final_request_opts()
        )
