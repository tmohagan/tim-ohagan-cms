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
async def test_playground_cpu_500():
    """Verify that both /fault/500 and /fault/cpu-500 trigger a simulated 500 crash."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r1 = await ac.get("/playground/fault/500")
        r2 = await ac.get("/playground/fault/cpu-500")
    assert r1.status_code == 500
    assert r1.json()["status"] == "error"
    assert r2.status_code == 500
    assert r2.json()["status"] == "error"

@pytest.mark.asyncio
async def test_playground_schema_422():
    """Verify that both /fault/422 and /fault/schema-422 simulate a schema validation 422 error."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r1 = await ac.get("/playground/fault/422")
        r2 = await ac.get("/playground/fault/schema-422")
    assert r1.status_code == 422
    assert "Schema Violation" in r1.json()["detail"]
    assert r2.status_code == 422
    assert "Schema Violation" in r2.json()["detail"]

@pytest.mark.asyncio
async def test_playground_db_deadlock():
    """Verify that /fault/db-deadlock simulates a database deadlock fault (500)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/playground/fault/db-deadlock")
    assert response.status_code == 500
    assert response.json()["status"] == "error"

@pytest.mark.asyncio
async def test_playground_memory_asset():
    """Verify that /fault/memory-asset simulates an asset memory exhaustion fault (500)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/playground/fault/memory-asset")
    assert response.status_code == 500
    assert response.json()["status"] == "error"

@pytest.mark.asyncio
async def test_serve_frontend():
    """Verify the premium frontend index.html is served correctly."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "<title>Tim O'Hagan" in response.text

@pytest.mark.asyncio
async def test_contact_inbox_requires_auth():
    """Verify that retrieving contact messages without authentication returns 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/contact/")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers

@pytest.mark.asyncio
async def test_admin_dashboard_requires_auth():
    """Verify that accessing /admin without authentication returns 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/admin")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_admin_dashboard_authenticated():
    """Verify that accessing /admin with valid Basic Auth returns 200 OK."""
    from app.core.security import ADMIN_USERNAME, ADMIN_PASSWORD
    auth = (ADMIN_USERNAME, ADMIN_PASSWORD)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/admin", auth=auth)
    assert response.status_code == 200
    assert "<title>Admin Dashboard" in response.text

@pytest.mark.asyncio
async def test_seed_requires_auth():
    """Verify that calling /seed without authentication returns 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/seed")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_favicon_ico():
    """Verify that /favicon.ico is served with HTTP 200."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/favicon.ico")
    assert response.status_code == 200
    assert len(response.content) > 0

@pytest.mark.asyncio
async def test_robots_txt():
    """Verify that /robots.txt is served with HTTP 200 and points to sitemap."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/robots.txt")
    assert response.status_code == 200
    assert "Sitemap: https://tim-ohagan.com/sitemap.xml" in response.text

@pytest.mark.asyncio
async def test_sitemap_xml():
    """Verify that /sitemap.xml is served with HTTP 200 and valid XML content."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")
    assert response.status_code == 200
    assert "https://tim-ohagan.com/" in response.text
    assert "application/xml" in response.headers.get("content-type", "")
