from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_200(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_shape(client: AsyncClient) -> None:
    data = (await client.get("/health")).json()
    assert "status" in data
    assert "version" in data
    assert "services" in data
    assert "database" in data["services"]
    assert "redis" in data["services"]
