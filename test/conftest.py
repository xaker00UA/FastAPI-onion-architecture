from fastapi.testclient import TestClient
from app.configurations.app import create_app
from app.configurations.db import init_db, drop_db
import pytest_asyncio
import pytest
from app.configurations.config import settings
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager


# app = create_app()


@pytest_asyncio.fixture(loop_scope="session", scope="session", autouse=True)
async def setup_db():
    assert settings.mode == "TEST"
    await drop_db()
    await init_db()
    yield
    # await drop_db()


@pytest_asyncio.fixture(loop_scope="session", scope="function")
async def client():
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver"
    ) as client:
        print("Client is ready")
        yield client
