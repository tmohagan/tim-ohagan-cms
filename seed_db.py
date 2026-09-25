import asyncio
from app.core.database import AsyncSessionLocal
from app.models.sql_models import Profile, Post, Comment

async def seed():
    async with AsyncSessionLocal() as session:
        # Create Profile
        tim_profile = Profile(
            name="Tim OHagan",
            bio="Software Agentic Engineer specializing in AI-driven autonomous Site Reliability Engineering.",
            github_url="https://github.com/tmohagan"
        )
        session.add(tim_profile)
        await session.commit()
        await session.refresh(tim_profile)
        print(f"Created Profile: {tim_profile.name} (ID: {tim_profile.id})")

        # Create Posts about GhostMachine.dev
        post1 = Post(
            title="Introducing GhostMachine.dev",
            content="""Imagine you run a website, and in the middle of the night, something breaks. Traditionally, an on-call engineer gets paged, wakes up, searches through server logs to figure out what went wrong, writes a bug fix, tests it, and pushes the repair live—a process that can easily take hours.

This project builds an automated "AI mechanic" designed to diagnose and repair software bugs on its own in under two minutes.

GhostMachine is an external autonomous SRE control plane that connects to target applications via webhooks. When an error is caught, it synthesizes a reproduction test, drafts a patch using LangGraph and LLMs, validates it via AST static analysis, runs the regression suite, and submits a PR to GitHub.
""",
            author_id=tim_profile.id
        )

        post2 = Post(
            title="The Deterministic Remediation Workflow",
            content="""GhostMachine relies on a highly structured LangGraph state machine to ensure safe and deterministic code repairs:

1. **Catch the Error**: The target website catches the crash and alerts GhostMachine via an OpenTelemetry webhook.
2. **Recreate the Problem**: GhostMachine writes a standalone test that deliberately reproduces the exact crash in an isolated Docker sandbox.
3. **Draft and Inspect**: An AI drafts a targeted code fix. Before it touches real code, a strict safety inspection tool checks the Python AST to guarantee no unsafe shortcuts were taken (e.g., disabling security checks).
4. **Test the Repair**: GhostMachine applies the fix inside the sandbox and runs the entire site's regression test suite.
5. **Submit the Work**: The system packages the fix into a formal GitHub Pull Request with a transparent receipt showing operational cost savings.
""",
            author_id=tim_profile.id
        )
        
        session.add_all([post1, post2])
        await session.commit()
        print("Created Posts about GhostMachine.dev")

if __name__ == "__main__":
    asyncio.run(seed())
