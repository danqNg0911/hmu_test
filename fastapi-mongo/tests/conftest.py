import pytest
from beanie import init_beanie
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient

from app import app, token_listener
from config.config import initiate_database
import models

async def mock_database():
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client["test_database"],
        recreate_views=True,
        document_models=models.__all__,
    )


def mock_no_authentication():
    app.dependency_overrides[token_listener] = lambda: {}


@pytest.fixture
async def client_test(mocker):
    """
    Create an instance of the client.
    :return: yield HTTP client.
    """

    mocker.patch("config.config.initiate_database", return_value=await mock_database())

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest.fixture
def anyio_backend():
    return "asyncio"
