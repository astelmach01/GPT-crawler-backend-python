import uuid
from typing import Any, AsyncGenerator
from unittest.mock import Mock

import pytest
from aio_pika import Channel
from aio_pika.abc import AbstractExchange, AbstractQueue
from aio_pika.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from .services.rabbit.dependencies import get_rmq_channel_pool
from .services.rabbit.lifetime import init_rabbit, shutdown_rabbit
from .web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: app name.
    """
    return "asyncio"


@pytest.fixture
async def test_rmq_pool() -> AsyncGenerator[Channel, None]:
    """
    Create rabbitMQ pool.

    :yield: channel pool.
    """
    app_mock = Mock()
    init_rabbit(app_mock)
    yield app_mock.state.rmq_channel_pool
    await shutdown_rabbit(app_mock)


@pytest.fixture
async def test_exchange_name() -> str:
    """
    Name of an exchange to use in tests.

    :return: name of an exchange.
    """
    return uuid.uuid4().hex


@pytest.fixture
async def test_routing_key() -> str:
    """
    Name of routing key to use while binding test queue.

    :return: key string.
    """
    return uuid.uuid4().hex


@pytest.fixture
async def test_exchange(
    test_exchange_name: str,
    test_rmq_pool: Pool[Channel],
) -> AsyncGenerator[AbstractExchange, None]:
    """
    Creates test exchange.

    :param test_exchange_name: name of an exchange to create.
    :param test_rmq_pool: channel pool for rabbitmq.
    :yield: created exchange.
    """
    async with test_rmq_pool.acquire() as conn:
        exchange = await conn.declare_exchange(
            name=test_exchange_name,
            auto_delete=True,
        )
        yield exchange

        await exchange.delete(if_unused=False)


@pytest.fixture
async def test_queue(
    test_exchange: AbstractExchange,
    test_rmq_pool: Pool[Channel],
    test_routing_key: str,
) -> AsyncGenerator[AbstractQueue, None]:
    """
    Creates queue connected to exchange.

    :param test_exchange: exchange to bind queue to.
    :param test_rmq_pool: channel pool for rabbitmq.
    :param test_routing_key: routing key to use while binding.
    :yield: queue binded to test exchange.
    """
    async with test_rmq_pool.acquire() as conn:
        queue = await conn.declare_queue(name=uuid.uuid4().hex)
        await queue.bind(
            exchange=test_exchange,
            routing_key=test_routing_key,
        )
        yield queue

        await queue.delete(if_unused=False, if_empty=False)


@pytest.fixture
def fastapi_app(
    test_rmq_pool: Pool[Channel],
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_rmq_channel_pool] = lambda: test_rmq_pool
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
