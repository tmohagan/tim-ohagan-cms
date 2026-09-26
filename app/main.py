from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import profile, playground, posts, comments, contact
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
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])

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

@app.get("/admin", tags=["Frontend"])
async def serve_admin():
    """Serve the admin dashboard."""
    return FileResponse("app/static/admin.html")

from sqlalchemy.future import select

POSTS_DATA = [
    {
        "title": "Introducing GhostMachine.dev",
        "content": "Imagine you run a website, and in the middle of the night, something breaks. Traditionally, an on-call engineer gets paged, wakes up, searches through server logs to figure out what went wrong, writes a bug fix, tests it, and pushes the repair live—a process that can easily take hours.\n\nThis project builds an automated \"AI mechanic\" designed to diagnose and repair software bugs on its own in under two minutes.\n\nGhostMachine is an external autonomous SRE control plane that connects to target applications via webhooks. When an error is caught, it synthesizes a reproduction test, drafts a patch using LangGraph and LLMs, validates it via AST static analysis, runs the regression suite, and submits a PR to GitHub."
    },
    {
        "title": "The Deterministic Remediation Workflow",
        "content": "GhostMachine relies on a highly structured LangGraph state machine to ensure safe and deterministic code repairs:\n\n1. **Catch the Error**: The target website catches the crash and alerts GhostMachine via an OpenTelemetry webhook.\n2. **Recreate the Problem**: GhostMachine writes a standalone test that deliberately reproduces the exact crash in an isolated Docker sandbox.\n3. **Draft and Inspect**: An AI drafts a targeted code fix. Before it touches real code, a strict safety inspection tool checks the Python AST to guarantee no unsafe shortcuts were taken (e.g., disabling security checks).\n4. **Test the Repair**: GhostMachine applies the fix inside the sandbox and runs the entire site's regression test suite.\n5. **Submit the Work**: The system packages the fix into a formal GitHub Pull Request with a transparent receipt showing operational cost savings."
    },
    {
        "title": "AST Static Guardrails: Zero-Trust Code Synthesis",
        "content": "When giving an LLM authority to propose code changes in an automated pipeline, prompt engineering is not enough. LLMs are prone to taking shortcuts—such as wrapping a crashing block in a bare `except:` block, which suppresses the symptom while corrupting application state downstream.\n\nTo enforce zero-trust security, GhostMachine integrates a compiler-level Abstract Syntax Tree (AST) validation node using Python's native `ast` module.\n\nEvery candidate unified diff is parsed into an in-memory syntax tree before execution:\n1. **Bare Except Detection**: The `SecurityAuditVisitor` inspects all `ExceptHandler` nodes. Any clause where `handler.type is None` triggers an immediate policy violation.\n2. **Namespace & Injection Whitelisting**: Candidate patches are audited for prohibited primitives (e.g., `os.system`, `subprocess`, or tampering with authentication decorators).\n3. **Patch Scope Constraints**: Diffs are hard-capped at 80 lines, ensuring the agent produces focused, surgical bug fixes rather than speculative architectural rewrites.\n\nBy validating AST nodes mathematically rather than relying on LLM self-policing, we ensure automated patches meet strict enterprise code review standards."
    },
    {
        "title": "Stateful Orchestration with LangGraph: Why Cyclic Graphs Beat Linear Scripts",
        "content": "Many early AI agent projects rely either on linear procedural scripts or open-ended ReAct loops. In autonomous SRE and infrastructure repair, both approaches fail: linear scripts cannot intelligently retry failed test runs, while unstructured loops frequently hallucinate into infinite execution cycles.\n\nGhostMachine solves this by architecting the incident pipeline as a typed **LangGraph StateGraph**:\n\n1. **Explicit State Schema (`IncidentState`)**: State is tracked across nodes with typed fields (`trace_id`, `stack_frames`, `repro_test_path`, `proposed_patch`, and `recursion_count`).\n2. **Deterministic State Reducers**: We bind recursion counters using `Annotated[int, operator.add]`. If an initial patch fails sandbox regression testing, the graph conditionally routes back to the patch synthesis node with the test failure output—capped at a strict maximum of 3 recursive cycles.\n3. **Reproducibility Verification**: Before generating a patch, GhostMachine requires that the generated `pytest` reproducing case fails in the isolated container (`sandbox_exit_code != 0`). If a test passes prematurely, the pipeline refuses to proceed.\n\nThis state-machine architecture provides the reliability required to automate tier-1 incident response safely."
    },
    {
        "title": "The Economics of Autonomous SRE: Slashing MTTR from 45 Minutes to 52 Seconds",
        "content": "Engineering on-call rotations are notorious for alert fatigue, context switching, and interrupted sleep. A routine tier-1 incident—such as an unhandled null pointer or schema validation error—typically costs an enterprise:\n\n• **45 to 60 minutes** of human investigation, git archaeology, and local environment reproduction.\n• **~$42.50** in direct engineering labor per incident (based on an $85/hr baseline).\n• Significant cognitive drag and deployment delays across the team.\n\nBy automating the diagnostic and remediation cycle, GhostMachine produces radical operational efficiencies:\n• **Mean Time to Remediation (MTTR)**: Drops from 45+ minutes to **52 seconds**.\n• **Inference & Compute Cost**: An average of 4,700 tokens across Gemini Flash models plus 38 seconds of sandbox container compute totals **$0.0263 per incident**.\n• **Net Operational Savings**: **+99.94%** per incident resolved.\n\nCrucially, GhostMachine does not replace human engineers—it acts as an automated mechanic. By delivering a validated patch, an ephemeral test suite, and an automated post-mortem directly to a GitHub Pull Request, engineers simply review and merge with high confidence."
    }
]

@app.post("/seed", tags=["System"])
async def seed_production_db(db: AsyncSession = Depends(get_db)):
    """Seed or update all showcase technical posts in the database."""
    # Create or retrieve Profile
    result = await db.execute(select(Profile).where(Profile.name == "Tim OHagan"))
    tim_profile = result.scalars().first()
    if not tim_profile:
        tim_profile = Profile(
            name="Tim OHagan",
            bio="Software Agentic Engineer specializing in AI-driven autonomous Site Reliability Engineering.",
            github_url="https://github.com/tmohagan"
        )
        db.add(tim_profile)
        await db.commit()
        await db.refresh(tim_profile)

    # Upsert Posts
    for post_info in POSTS_DATA:
        res = await db.execute(select(Post).where(Post.title == post_info["title"]))
        existing_post = res.scalars().first()
        if not existing_post:
            new_post = Post(
                title=post_info["title"],
                content=post_info["content"],
                author_id=tim_profile.id
            )
            db.add(new_post)
        else:
            existing_post.content = post_info["content"]

    await db.commit()
    return {"status": "success", "message": "All showcase posts seeded and updated successfully."}
