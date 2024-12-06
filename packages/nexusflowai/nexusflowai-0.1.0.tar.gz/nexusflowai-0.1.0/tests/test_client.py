from os import environ

from pytest import fixture

from nexusflowai import NexusflowAI, AsyncNexusflowAI
from tests.utils import BASE_URL, API_KEY


class TestNexusflowAI:
    @fixture
    def setup_client(self) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = NexusflowAI(base_url=BASE_URL)

    def test_sanity(self, setup_client):
        client = self.client
        assert client.api_key == environ["NEXUSFLOWAI_API_KEY"]
        assert client.organization == None
        assert str(client.base_url) == BASE_URL


class TestAsyncNexusflowAI:
    @fixture
    def setup_client(self) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = AsyncNexusflowAI(base_url=BASE_URL)

    def test_sanity(self, setup_client):
        client = self.client
        assert client.api_key == environ["NEXUSFLOWAI_API_KEY"]
        assert client.organization == None
        assert str(client.base_url) == BASE_URL
