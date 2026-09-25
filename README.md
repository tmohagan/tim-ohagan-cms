# Tim O'Hagan CMS

Tim O'Hagan CMS is a reference target Content Management System (CMS) built to demonstrate the capabilities of **GhostMachine SRE**, an autonomous Site Reliability Engineering system. It serves as the primary testing ground and target application for fault injection, detection, and autonomous remediation.

## Overview

The CMS is built using modern Python web technologies to simulate a real-world production application. It incorporates specialized middleware (`GhostMachineMiddleware`) designed to capture exceptions and route them directly to the GhostMachine control plane for analysis and automated patching.

## Technology Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (via asyncpg)
- **ORM**: SQLAlchemy 2.0 with Alembic for migrations
- **Caching**: Redis
- **Containerization**: Docker & Docker Compose
- **Configuration**: Pydantic Settings

## Key Features

- **Profile API**: Endpoints for managing user profile content.
- **Chaos Playground**: A dedicated set of endpoints (`/playground`) designed for testing fault injection and adversarial scenarios.
- **GhostMachine Integration**: Custom middleware that hooks into the application's lifecycle to intercept uncaught exceptions and report them to the autonomous SRE pipeline.

## Getting Started

To run the CMS locally:

1. Clone the repository.
2. Build and start the services using Docker Compose:
   ```bash
   docker compose up --build -d
   ```
3. The API will be available at `http://localhost:8000`. You can explore the interactive API documentation at `http://localhost:8000/docs`.

## Integration with GhostMachine

This repository is strictly the **target application**. When errors occur within this CMS (e.g., triggered via the Chaos Playground), the `GhostMachineMiddleware` captures the trace and sends a webhook to the `ghostmachine-core` control plane. GhostMachine then:
1. Analyzes the fault using LLMs.
2. Synthesizes a patch for this repository.
3. Automatically opens a Pull Request to resolve the issue.

For details on the SRE agent itself, refer to the [ghostmachine-core](https://github.com/tmohagan/ghostmachine-core) repository.
