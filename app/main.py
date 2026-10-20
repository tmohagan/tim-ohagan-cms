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
    title="Tim O'Hagan - Forward Deployment Engineering",
    description="Portfolio and CMS for Forward Deployment Engineering with Autonomous AI Agents",
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

from app.core.security import get_current_admin

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/robots.txt", include_in_schema=False)
async def serve_robots():
    return FileResponse("app/static/robots.txt")

@app.get("/sitemap.xml", include_in_schema=False)
async def serve_sitemap():
    return FileResponse("app/static/sitemap.xml", media_type="application/xml")

@app.get("/", tags=["Frontend"])
async def serve_frontend():
    """Serve the premium portfolio frontend."""
    return FileResponse("app/static/index.html")

@app.get("/admin", tags=["Frontend"])
async def serve_admin(admin: str = Depends(get_current_admin)):
    """Serve the admin dashboard, protected by HTTP Basic Auth."""
    return FileResponse("app/static/admin.html")

from sqlalchemy.future import select
from sqlalchemy import delete

POSTS_DATA = [
    {
        "title": "The Rise of the Forward Deployment Engineer in the Agentic AI Era",
        "category": "Autonomous SRE",
        "content": "The rapid progression of frontier foundation models has fundamentally shifted the bottleneck in enterprise AI from model capabilities to field execution. While research labs release increasingly capable reasoning models, enterprise clients struggle with the \"last mile\" problem: embedding autonomous agentic workflows into legacy infrastructures, secure VPCs, and mission-critical operational loops.\n\nEnter the **Forward Deployment Engineer (FDE)** for AI Agents.\n\nBorrowing from the field-engineering ethos pioneered in mission-driven tech, the Agentic FDE operates directly at the fault line between cutting-edge autonomous agents and customer realities:\n1. **Context Extraction & Schema Mapping**: Transforming unstructured client data and legacy database schemas into high-fidelity context windows and Model Context Protocol (MCP) tool endpoints.\n2. **Autonomous SRE & Self-Healing Integration**: Deploying supervisory agents (such as GhostMachine) into client cloud environments to monitor live microservices, catch unhandled exceptions, and synthesize pull requests within seconds.\n3. **Guardrails Over Blind Faith**: Replacing fragile prompt engineering with compiler-enforced Abstract Syntax Tree (AST) validation and gVisor sandboxing to satisfy stringent enterprise InfoSec and compliance requirements.\n\nRather than selling canned APIs, the modern FDE ships resilient, production-hardened agent architectures that drive quantifiable business impact on Day 1."
    },
    {
        "title": "Productionizing AI Agents: Bridging Frontier Models to Mission-Critical Enterprise Stacks",
        "category": "Agentic Architecture",
        "content": "Deploying a demonstration agent in a notebook is trivial; keeping an autonomous multi-agent swarm stable inside an enterprise Kubernetes cluster is an engineering discipline in its infancy.\n\nWhen forward deploying AI agents into client environments, three architectural pillars separate toy scripts from production systems:\n\n1. **Stateful Graph Orchestration (LangGraph)**:\nUnstructured ReAct loops inevitably get stuck in recursive spirals. By modeling client workflows as cyclic directed graphs with typed state (`IncidentState`), deterministic state reducers, and hard recursion bounds (e.g. maximum 3 retries), the agent behaves with deterministic predictability.\n\n2. **Standardized Tool Interoperability (MCP)**:\nInstead of bespoke API wrappers that decay with client updates, we leverage standardized tool calling schemas via the Model Context Protocol (MCP). Agents discover client tools dynamically, validate arguments against strict Pydantic models, and execute remote procedures through secure reverse proxies.\n\n3. **Human-in-the-Loop (HITL) Checkpointing**:\nHigh-stakes operations (modifying database records, provisioning cloud infrastructure, merging code into production) must support asynchronous pause-and-resume. By persisting graph state in PostgreSQL checkpointers (`PostgresSaver`), field engineers can inject human sign-offs before destructive actions execute.\n\nThis deterministic foundation is what allows enterprises to entrust autonomous agents with critical business workflows."
    },
    {
        "title": "Autonomous Incident Remediation as an Enterprise Service: Deploying SRE Agents in Client VPCs",
        "category": "Autonomous SRE",
        "content": "When client enterprise services experience unhandled crashes during off-peak hours, the traditional escalation path is brutally inefficient: an on-call engineer is paged, context-switches, digs through distributed logs, clones the repository, attempts to reproduce the fault, writes a patch, and waits for CI/CD—resulting in an average MTTR of 45 to 60 minutes.\n\nThrough forward deployed SRE agents, we transform this operational drag into a deterministic, automated loop:\n\n• **Zero Data Egress**: The telemetry middleware (`GhostMachineMiddleware`) captures in-memory stack frames, scrubs sensitive client authorization headers, and fires signed webhooks strictly within the client's private network or encrypted ingress.\n• **Instant Test Synthesis**: An isolated reproduction subagent parses the stack frame and drafts a standalone pytest script reproducing the exact crash vector.\n• **Ephemeral Sandbox Verification**: Running inside a gVisor-isolated container, the test verifies the bug (`exit_code != 0`), synthesizes an AST-verified patch, and confirms regression pass (`exit_code == 0`).\n• **Economics of Automation**: Slashing MTTR from 45 minutes to 52 seconds reduces tier-1 incident handling cost from ~$42.50 in human engineering labor to $0.0263 in inference and sandbox compute—yielding a 99.94% reduction in operational spend."
    },
    {
        "title": "Field-Testing Agent Reliability: Synthetic Chaos Engineering in Customer Sandboxes",
        "category": "Chaos Engineering",
        "content": "How do forward deployment engineers prove to client CTOs and risk committees that an autonomous agent will not hallucinate catastrophic failures during a production outage?\n\nYou test it in battle before going live.\n\nIn our customer deployment playbook, we embed a dedicated **Chaos Playground** into the staging environment:\n1. **CPU & Unhandled Exception Injection (`/fault/cpu-500`)**: Forces divide-by-zero crashes to confirm the telemetry capture layer intercepts the error and dispatches signed webhooks in real time.\n2. **Schema Validation Drifts (`/fault/schema-422`)**: Simulates breaking API payload changes to ensure the agent synthesizes robust fallback models rather than failing silently.\n3. **Database Deadlocks & Contention (`/fault/db-deadlock`)**: Simulates concurrent asyncpg row lock timeouts, validating that the agent diagnoses database connection pool exhaustion and applies exponential backoff logic.\n4. **Memory Spikes & Asset Exhaustion (`/fault/memory-asset`)**: Injects buffer allocation limits to test how the agent refactors synchronous read operations into streamed backpressure pipelines.\n\nBy validating agentic repair pipelines against synthetic chaos vectors, client engineering teams develop the confidence needed to grant agents production autonomy."
    },
    {
        "title": "Enterprise Guardrails & AST Compilation: Delivering Zero-Trust Agent Code into Production",
        "category": "AI Security & Guardrails",
        "content": "Enterprise InfoSec teams are rightly skeptical when told an LLM will automatically generate code and open pull requests against production repositories. Natural language system prompts (\"Please write safe code and never remove auth checks\") provide zero security guarantees against adversarial inputs or model hallucinations.\n\nTo achieve enterprise acceptance, Forward Deployment Engineers enforce **compiler-enforced, zero-trust AST guardrails**:\n\n1. **AST Parsing Before Disk Writes**:\nEvery unified diff generated by the patch agent is parsed in memory using Python's native `ast` compiler before any filesystem mutation occurs.\n\n2. **Prohibited Primitive Blacklisting**:\nA custom `SecurityAuditVisitor` inspects every syntactic node. Calls to `os.system`, `subprocess`, `exec`, or `eval` trigger immediate aborts.\n\n3. **Bare Exception Elimination**:\nOne of the most dangerous LLM coding patterns is catching all exceptions (`except: pass`), which masks root failures and corrupts downstream state. Our AST guardrail immediately rejects any `ExceptHandler` with `handler.type is None`.\n\n4. **Diff Scope Enforcement**:\nCandidate diffs are hard-capped at 80 lines. This forces the agent to deliver surgical, reviewable fixes rather than attempting wide, unverified refactors.\n\nWhen security policies are mathematical compiler invariants rather than prompt suggestions, enterprise security teams enthusiastically greenlight agent deployments."
    },
    {
        "title": "The FDE Playbook: Evaluation Harnesses, Drift Detection, and Day-2 Operations for Agents",
        "category": "Agentic Architecture",
        "content": "Getting an agent to complete a workflow on Day 1 is only 20% of the forward deployment engagement. Day-2 operations—maintaining accuracy as customer APIs drift, schemas change, and edge cases accumulate—dictates whether an agent system survives in the enterprise.\n\nThe modern FDE operates with a rigorous Day-2 evaluation playbook:\n\n• **Ground-Truth Eval Harnesses**: We build offline benchmark suites reflecting historical client failure cases and domain-specific edge scenarios. Every prompt update or model migration runs through headless evaluation matrices before deployment.\n• **Drift & Semantic Hallucination Monitoring**: Real-time telemetry tracks tool-calling accuracy, schema validation rejection rates, and context retrieval relevance scores.\n• **Economic Telemetry Ledger**: Client executives require clear proof of value. We embed automated telemetry tracking token consumption, model inference costs, and container execution times, dynamically comparing operational costs against human engineering baselines.\n• **Time-Travel Incident Replays**: With state durably persisted in PostgreSQL checkpointers, client teams can inspect exact intermediate states, token inputs, and agent reasoning traces at every step of historical executions."
    },
    {
        "title": "Hardening gVisor Container Sandboxes for Client-Side Code Synthesis",
        "category": "Chaos Engineering",
        "content": "When deploying agents that write and execute tests autonomously on client infrastructure, standard container isolation (e.g. Docker runc) is insufficient. Standard Docker containers share the host Linux kernel; a malicious or hallucinated command inside a generated test could theoretically trigger kernel privilege escalations.\n\nTo deliver zero-trust isolation on client hardware, we architect the execution sandbox using Google's **gVisor (`runsc`)**:\n\n1. **User-Space Kernel Interception**:\ngVisor implements an independent user-space Linux kernel written in Go. System calls originating from AI-generated pytest scripts are intercepted by `runsc` rather than directly hitting the host OS kernel.\n\n2. **Resource Throttling**:\nContainers are bounded with strict resource ceilings (`mem_limit=\"2048m\"`, `nano_cpus=2000000000`, network-isolated bridge interfaces) to prevent rogue recursive processes or memory exhaustion.\n\n3. **Safe Directory Git Mounting**:\nTo allow safe diff application without file permission corruption across Docker volume boundaries, staging nodes automatically configure `git config --global --add safe.directory <repo_path>` inside the isolated context.\n\nThis dual-layer isolation (Docker + gVisor) provides enterprise security teams with the assurance that agent test execution remains strictly hermetic."
    },
    {
        "title": "Client-Centric Telemetry: Designing OpenTelemetry Pipelines for Agent Observability",
        "category": "AI Security & Guardrails",
        "content": "Observability is the lifeblood of forward deployment engineering. When an autonomous agent acts on behalf of enterprise users, developers and compliance officers must be able to trace every decision back to its root cause.\n\nIn our production deployments, we architect end-to-end OpenTelemetry (OTel) pipelines tailored for agentic interactions:\n\n• **Boundary PII & Secret Scrubbing**: The telemetry middleware automatically scrubs sensitive request headers (`Authorization`, `Cookie`, `X-Api-Key`, `X-GhostMachine-Secret`) at the network boundary before payloads are serialized or transmitted.\n• **Distributed Trace Correlation**: Incoming web requests carry `x-b3-traceid` identifiers that propagate through the entire remediation lifecycle—linking the initial customer HTTP fault to the LLM prompt, the Docker sandbox execution logs, and the resulting GitHub pull request.\n• **Constant-Time Cryptographic Verification**: Inter-service webhooks between client applications and the agent control plane are signed with high-entropy shared secrets and verified using constant-time string hashing (`secrets.compare_digest`), thwarting timing attacks.\n\nBy prioritizing end-to-end observability and rigorous redaction, forward deployment engineers ensure enterprise AI remains auditable, compliant, and transparent."
    }
]

@app.post("/seed", tags=["System"])
async def seed_production_db(
    db: AsyncSession = Depends(get_db),
    admin: str = Depends(get_current_admin)
):
    """Seed or update all showcase technical posts in the database. Protected by admin authentication."""
    # Create or update Profile
    result = await db.execute(select(Profile).where(Profile.name == "Tim OHagan"))
    tim_profile = result.scalars().first()
    if not tim_profile:
        tim_profile = Profile(
            name="Tim OHagan",
            bio="Forward Deployment Engineer deploying autonomous AI agent systems and self-healing cloud infrastructure into enterprise environments.",
            github_url="https://github.com/tmohagan"
        )
        db.add(tim_profile)
        await db.commit()
        await db.refresh(tim_profile)
    else:
        tim_profile.bio = "Forward Deployment Engineer deploying autonomous AI agent systems and self-healing cloud infrastructure into enterprise environments."
        await db.commit()

    # Clear existing posts to replace with Forward Deployment Engineering posts
    await db.execute(delete(Post))
    await db.commit()

    # Insert Posts
    for post_info in POSTS_DATA:
        new_post = Post(
            title=post_info["title"],
            category=post_info.get("category", "Autonomous SRE"),
            content=post_info["content"],
            author_id=tim_profile.id
        )
        db.add(new_post)

    await db.commit()
    return {"status": "success", "message": "All Forward Deployment Engineering posts seeded successfully."}
