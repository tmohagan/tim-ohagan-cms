from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import profile, playground, posts, comments
from app.core.middleware import GhostMachineMiddleware
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql_models import Profile, Post

# Instantiate the root application object in RAM
app = FastAPI(
    title="Tim O'Hagan CMS",
    description="Reference Target Capstone for Autonomous SRE",
    version="1.0.0"
)

# Bind the custom GhostMachine exception capture middleware
app.add_middleware(GhostMachineMiddleware)

# Bind the routers to the root application's lookup table
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(playground.router, prefix="/playground", tags=["Chaos"])

@app.get("/health", tags=["System"])
async def health_check():
    """Deterministic pulse check to verify the process is alive."""
    return {"status": "ok", "service": "tim-ohagan-cms"}

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", tags=["Frontend"])
async def serve_frontend():
    """Serve the premium portfolio frontend."""
    return FileResponse("app/static/index.html")

@app.post("/seed", tags=["System"])
async def seed_production_db(db: AsyncSession = Depends(get_db)):
    """Temporary endpoint to seed the production database."""
    # Create Profile
    tim_profile = Profile(
        name="Tim OHagan",
        bio="Software Agentic Engineer specializing in AI-driven autonomous Site Reliability Engineering.",
        github_url="https://github.com/tmohagan"
    )
    db.add(tim_profile)
    await db.commit()
    await db.refresh(tim_profile)

    # Create Posts
    post1 = Post(
        title="Introducing GhostMachine.dev",
        content="Imagine you run a website, and in the middle of the night, something breaks. Traditionally, an on-call engineer gets paged, wakes up, searches through server logs to figure out what went wrong, writes a bug fix, tests it, and pushes the repair live—a process that can easily take hours.\n\nThis project builds an automated \"AI mechanic\" designed to diagnose and repair software bugs on its own in under two minutes.\n\nGhostMachine is an external autonomous SRE control plane that connects to target applications via webhooks. When an error is caught, it synthesizes a reproduction test, drafts a patch using LangGraph and LLMs, validates it via AST static analysis, runs the regression suite, and submits a PR to GitHub.",
        author_id=tim_profile.id
    )

    post2 = Post(
        title="The Deterministic Remediation Workflow",
        content="GhostMachine relies on a highly structured LangGraph state machine to ensure safe and deterministic code repairs:\n\n1. **Catch the Error**: The target website catches the crash and alerts GhostMachine via an OpenTelemetry webhook.\n2. **Recreate the Problem**: GhostMachine writes a standalone test that deliberately reproduces the exact crash in an isolated Docker sandbox.\n3. **Draft and Inspect**: An AI drafts a targeted code fix. Before it touches real code, a strict safety inspection tool checks the Python AST to guarantee no unsafe shortcuts were taken (e.g., disabling security checks).\n4. **Test the Repair**: GhostMachine applies the fix inside the sandbox and runs the entire site's regression test suite.\n5. **Submit the Work**: The system packages the fix into a formal GitHub Pull Request with a transparent receipt showing operational cost savings.",
        author_id=tim_profile.id
    )
    
    db.add_all([post1, post2])
    await db.commit()
    return {"status": "success", "message": "Production database seeded successfully."}
