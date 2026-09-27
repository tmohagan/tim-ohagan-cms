# Tim O'Hagan Portfolio & CMS

[![Live Production](https://img.shields.io/badge/Live-tim--ohagan.com-00ffff?style=flat-square)](https://tim-ohagan.com)
[![Monitored By](https://img.shields.io/badge/Monitored%20By-GhostMachine.dev-3fb950?style=flat-square)](https://ghostmachine.dev)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

Portfolio and Content Management System for **Tim O'Hagan** (Software Agentic Engineer), serving as the reference target application for [GhostMachine.dev](https://ghostmachine.dev)—an autonomous Site Reliability Engineering (SRE) control plane.

---

## Live Endpoints

- **Production URL**: [https://tim-ohagan.com](https://tim-ohagan.com) (Canonical)
- **Subdomain**: [https://www.tim-ohagan.com](https://www.tim-ohagan.com) (Automated 301 Redirect)
- **Chaos Playground**: [https://tim-ohagan.com/#playground](https://tim-ohagan.com/#playground)
- **Technical Transmissions**: [https://tim-ohagan.com/#posts](https://tim-ohagan.com/#posts)

---

## Architecture & Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Async Python 3.11+)
- **Database & ORM**: PostgreSQL 15 via `asyncpg` with [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **In-Memory Cache**: Redis 7
- **Authentication**: HTTP Basic Auth with constant-time string hashing (`secrets.compare_digest`)
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphic dark design system), SPA hash routing
- **Ingress & TLS**: Reverse-proxied via Caddy 2 with automatic Let's Encrypt TLS and HSTS

---

## Key Features

### 1. Interactive Chaos Playground (`/#playground`)
Demonstrates real-time error interception and autonomous remediation. Includes 4 distinct failure vectors:
- **CPU Fault (`/playground/fault/cpu-500`)**: Forces an unhandled divide-by-zero exception to test runtime crash interception.
- **Schema Violation (`/playground/fault/schema-422`)**: Simulates malformed payload structure and missing schema attributes.
- **DB Deadlock (`/playground/fault/db-deadlock`)**: Simulates concurrent row lock contention on PostgreSQL transactions.
- **Asset Exhaustion (`/playground/fault/memory-asset`)**: Simulates buffer allocation memory spikes and out-of-memory limits.

### 2. Autonomous Telemetry Middleware (`GhostMachineMiddleware`)
Custom Starlette/FastAPI middleware that intercepts uncaught application crashes:
- Extracts or generates OpenTelemetry-compatible trace IDs (`x-b3-traceid`).
- Formats in-memory stack frames and TCP context.
- **Security Redaction**: Automatically scrubs sensitive headers (`Authorization`, `Cookie`, `X-Api-Key`, `X-GhostMachine-Secret`).
- **Authenticated Outbound Webhook**: Attaches `X-GhostMachine-Secret` and dispatches telemetry asynchronously to the GhostMachine control plane.

### 3. Protected Contact Inbox & Admin Dashboard (`/admin`)
- Contact messages submitted via the public contact modal are stored securely in PostgreSQL.
- Access to `GET /api/contact/`, `/admin`, and `POST /seed` is strictly gated behind HTTP Basic Authentication (`get_current_admin`).

### 4. SEO & Social Previews
- **OpenGraph & Twitter Cards**: High-resolution 1200x630 preview card (`/static/og-image.png`).
- **Favicons**: Multi-format dark mode icons (`favicon.svg` and `favicon.ico`).
- **Search Engine Discovery**: Dedicated endpoints for `/robots.txt` and `/sitemap.xml`.

---

## Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL asyncpg connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis cache connection string | `redis://cms-redis:6379/0` |
| `GHOSTMACHINE_WEBHOOK_URL` | Outbound telemetry endpoint on control plane | `http://ghostmachine.local:8000/api/webhooks` |
| `WEBHOOK_SECRET` | Shared secret sent in `X-GhostMachine-Secret` | Required in production |
| `ADMIN_USERNAME` | Username for `/admin` and `/api/contact/` | `admin` |
| `ADMIN_PASSWORD` | Password for administrative access | Required in production |

---

## Local Development & Testing

### Running with Docker Compose
```bash
# Start all services (app, postgres, redis)
docker compose up --build -d

# Verify services are running
docker compose ps
```

The application will be accessible at `http://localhost:8000`.

### Running Unit & Security Tests
```bash
# Run tests inside the running container
docker exec cms-app pytest -v

# Or run locally via Poetry
poetry run pytest -v
```

---

## License

MIT License. Designed and maintained by [Tim O'Hagan](https://github.com/tmohagan).
