import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """Verify the root health check endpoint returns 200 OK and expected JSON."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "tim-ohagan-cms"}

@pytest.mark.asyncio
async def test_playground_422():
    """Verify the chaos playground successfully simulates a 422 error."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/playground/fault/422")
    assert response.status_code == 422
    assert response.json() == {"detail": "Simulated Unprocessable Entity"}

@pytest.mark.asyncio
async def test_serve_frontend():
    """Verify the premium frontend index.html is served correctly."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "<title>Tim O'Hagan" in response.text
