import asyncio
from app.core.database import AsyncSessionLocal
from app.models.sql_models import Profile, Post, Comment
from sqlalchemy.future import select
from sqlalchemy import delete

POSTS_DATA = [
    {
        "title": "The Rise of the Forward Deployment Engineer in the Agentic AI Era",
        "category": "Autonomous SRE",
        "content": """The rapid progression of frontier foundation models has fundamentally shifted the bottleneck in enterprise AI from model capabilities to field execution. While research labs release increasingly capable reasoning models, enterprise clients struggle with the "last mile" problem: embedding autonomous agentic workflows into legacy infrastructures, secure VPCs, and mission-critical operational loops.

Enter the **Forward Deployment Engineer (FDE)** for AI Agents.

Borrowing from the field-engineering ethos pioneered in mission-driven tech, the Agentic FDE operates directly at the fault line between cutting-edge autonomous agents and customer realities:
1. **Context Extraction & Schema Mapping**: Transforming unstructured client data and legacy database schemas into high-fidelity context windows and Model Context Protocol (MCP) tool endpoints.
2. **Autonomous SRE & Self-Healing Integration**: Deploying supervisory agents (such as GhostMachine) into client cloud environments to monitor live microservices, catch unhandled exceptions, and synthesize pull requests within seconds.
3. **Guardrails Over Blind Faith**: Replacing fragile prompt engineering with compiler-enforced Abstract Syntax Tree (AST) validation and gVisor sandboxing to satisfy stringent enterprise InfoSec and compliance requirements.

Rather than selling canned APIs, the modern FDE ships resilient, production-hardened agent architectures that drive quantifiable business impact on Day 1."""
    },
    {
        "title": "Productionizing AI Agents: Bridging Frontier Models to Mission-Critical Enterprise Stacks",
        "category": "Agentic Architecture",
        "content": """Deploying a demonstration agent in a notebook is trivial; keeping an autonomous multi-agent swarm stable inside an enterprise Kubernetes cluster is an engineering discipline in its infancy.

When forward deploying AI agents into client environments, three architectural pillars separate toy scripts from production systems:

1. **Stateful Graph Orchestration (LangGraph)**:
Unstructured ReAct loops inevitably get stuck in recursive spirals. By modeling client workflows as cyclic directed graphs with typed state (`IncidentState`), deterministic state reducers, and hard recursion bounds (e.g. maximum 3 retries), the agent behaves with deterministic predictability.

2. **Standardized Tool Interoperability (MCP)**:
Instead of bespoke API wrappers that decay with client updates, we leverage standardized tool calling schemas via the Model Context Protocol (MCP). Agents discover client tools dynamically, validate arguments against strict Pydantic models, and execute remote procedures through secure reverse proxies.

3. **Human-in-the-Loop (HITL) Checkpointing**:
High-stakes operations (modifying database records, provisioning cloud infrastructure, merging code into production) must support asynchronous pause-and-resume. By persisting graph state in PostgreSQL checkpointers (`PostgresSaver`), field engineers can inject human sign-offs before destructive actions execute.

This deterministic foundation is what allows enterprises to entrust autonomous agents with critical business workflows."""
    },
    {
        "title": "Autonomous Incident Remediation as an Enterprise Service: Deploying SRE Agents in Client VPCs",
        "category": "Autonomous SRE",
        "content": """When client enterprise services experience unhandled crashes during off-peak hours, the traditional escalation path is brutally inefficient: an on-call engineer is paged, context-switches, digs through distributed logs, clones the repository, attempts to reproduce the fault, writes a patch, and waits for CI/CD—resulting in an average MTTR of 45 to 60 minutes.

Through forward deployed SRE agents, we transform this operational drag into a deterministic, automated loop:

• **Zero Data Egress**: The telemetry middleware (`GhostMachineMiddleware`) captures in-memory stack frames, scrubs sensitive client authorization headers, and fires signed webhooks strictly within the client's private network or encrypted ingress.
• **Instant Test Synthesis**: An isolated reproduction subagent parses the stack frame and drafts a standalone pytest script reproducing the exact crash vector.
• **Ephemeral Sandbox Verification**: Running inside a gVisor-isolated container, the test verifies the bug (`exit_code != 0`), synthesizes an AST-verified patch, and confirms regression pass (`exit_code == 0`).
• **Economics of Automation**: Slashing MTTR from 45 minutes to 52 seconds reduces tier-1 incident handling cost from ~$42.50 in human engineering labor to $0.0263 in inference and sandbox compute—yielding a 99.94% reduction in operational spend."""
    },
    {
        "title": "Field-Testing Agent Reliability: Synthetic Chaos Engineering in Customer Sandboxes",
        "category": "Chaos Engineering",
        "content": """How do forward deployment engineers prove to client CTOs and risk committees that an autonomous agent will not hallucinate catastrophic failures during a production outage?

You test it in battle before going live.

In our customer deployment playbook, we embed a dedicated **Chaos Playground** into the staging environment:
1. **CPU & Unhandled Exception Injection (`/fault/cpu-500`)**: Forces divide-by-zero crashes to confirm the telemetry capture layer intercepts the error and dispatches signed webhooks in real time.
2. **Schema Validation Drifts (`/fault/schema-422`)**: Simulates breaking API payload changes to ensure the agent synthesizes robust fallback models rather than failing silently.
3. **Database Deadlocks & Contention (`/fault/db-deadlock`)**: Simulates concurrent asyncpg row lock timeouts, validating that the agent diagnoses database connection pool exhaustion and applies exponential backoff logic.
4. **Memory Spikes & Asset Exhaustion (`/fault/memory-asset`)**: Injects buffer allocation limits to test how the agent refactors synchronous read operations into streamed backpressure pipelines.

By validating agentic repair pipelines against synthetic chaos vectors, client engineering teams develop the confidence needed to grant agents production autonomy."""
    },
    {
        "title": "Enterprise Guardrails & AST Compilation: Delivering Zero-Trust Agent Code into Production",
        "category": "AI Security & Guardrails",
        "content": """Enterprise InfoSec teams are rightly skeptical when told an LLM will automatically generate code and open pull requests against production repositories. Natural language system prompts ("Please write safe code and never remove auth checks") provide zero security guarantees against adversarial inputs or model hallucinations.

To achieve enterprise acceptance, Forward Deployment Engineers enforce **compiler-enforced, zero-trust AST guardrails**:

1. **AST Parsing Before Disk Writes**:
Every unified diff generated by the patch agent is parsed in memory using Python's native `ast` compiler before any filesystem mutation occurs.

2. **Prohibited Primitive Blacklisting**:
A custom `SecurityAuditVisitor` inspects every syntactic node. Calls to `os.system`, `subprocess`, `exec`, or `eval` trigger immediate aborts.

3. **Bare Exception Elimination**:
One of the most dangerous LLM coding patterns is catching all exceptions (`except: pass`), which masks root failures and corrupts downstream state. Our AST guardrail immediately rejects any `ExceptHandler` with `handler.type is None`.

4. **Diff Scope Enforcement**:
Candidate diffs are hard-capped at 80 lines. This forces the agent to deliver surgical, reviewable fixes rather than attempting wide, unverified refactors.

When security policies are mathematical compiler invariants rather than prompt suggestions, enterprise security teams enthusiastically greenlight agent deployments."""
    },
    {
        "title": "The FDE Playbook: Evaluation Harnesses, Drift Detection, and Day-2 Operations for Agents",
        "category": "Agentic Architecture",
        "content": """Getting an agent to complete a workflow on Day 1 is only 20% of the forward deployment engagement. Day-2 operations—maintaining accuracy as customer APIs drift, schemas change, and edge cases accumulate—dictates whether an agent system survives in the enterprise.

The modern FDE operates with a rigorous Day-2 evaluation playbook:

• **Ground-Truth Eval Harnesses**: We build offline benchmark suites reflecting historical client failure cases and domain-specific edge scenarios. Every prompt update or model migration runs through headless evaluation matrices before deployment.
• **Drift & Semantic Hallucination Monitoring**: Real-time telemetry tracks tool-calling accuracy, schema validation rejection rates, and context retrieval relevance scores.
• **Economic Telemetry Ledger**: Client executives require clear proof of value. We embed automated telemetry tracking token consumption, model inference costs, and container execution times, dynamically comparing operational costs against human engineering baselines.
• **Time-Travel Incident Replays**: With state durably persisted in PostgreSQL checkpointers, client teams can inspect exact intermediate states, token inputs, and agent reasoning traces at every step of historical executions."""
    },
    {
        "title": "Hardening gVisor Container Sandboxes for Client-Side Code Synthesis",
        "category": "Chaos Engineering",
        "content": """When deploying agents that write and execute tests autonomously on client infrastructure, standard container isolation (e.g. Docker runc) is insufficient. Standard Docker containers share the host Linux kernel; a malicious or hallucinated command inside a generated test could theoretically trigger kernel privilege escalations.

To deliver zero-trust isolation on client hardware, we architect the execution sandbox using Google's **gVisor (`runsc`)**:

1. **User-Space Kernel Interception**:
gVisor implements an independent user-space Linux kernel written in Go. System calls originating from AI-generated pytest scripts are intercepted by `runsc` rather than directly hitting the host OS kernel.

2. **Resource Throttling**:
Containers are bounded with strict resource ceilings (`mem_limit="2048m"`, `nano_cpus=2000000000`, network-isolated bridge interfaces) to prevent rogue recursive processes or memory exhaustion.

3. **Safe Directory Git Mounting**:
To allow safe diff application without file permission corruption across Docker volume boundaries, staging nodes automatically configure `git config --global --add safe.directory <repo_path>` inside the isolated context.

This dual-layer isolation (Docker + gVisor) provides enterprise security teams with the assurance that agent test execution remains strictly hermetic."""
    },
    {
        "title": "Client-Centric Telemetry: Designing OpenTelemetry Pipelines for Agent Observability",
        "category": "AI Security & Guardrails",
        "content": """Observability is the lifeblood of forward deployment engineering. When an autonomous agent acts on behalf of enterprise users, developers and compliance officers must be able to trace every decision back to its root cause.

In our production deployments, we architect end-to-end OpenTelemetry (OTel) pipelines tailored for agentic interactions:

• **Boundary PII & Secret Scrubbing**: The telemetry middleware automatically scrubs sensitive request headers (`Authorization`, `Cookie`, `X-Api-Key`, `X-GhostMachine-Secret`) at the network boundary before payloads are serialized or transmitted.
• **Distributed Trace Correlation**: Incoming web requests carry `x-b3-traceid` identifiers that propagate through the entire remediation lifecycle—linking the initial customer HTTP fault to the LLM prompt, the Docker sandbox execution logs, and the resulting GitHub pull request.
• **Constant-Time Cryptographic Verification**: Inter-service webhooks between client applications and the agent control plane are signed with high-entropy shared secrets and verified using constant-time string hashing (`secrets.compare_digest`), thwarting timing attacks.

By prioritizing end-to-end observability and rigorous redaction, forward deployment engineers ensure enterprise AI remains auditable, compliant, and transparent."""
    }
]

async def seed():
    async with AsyncSessionLocal() as session:
        # Check or Create Profile
        result = await session.execute(select(Profile).where(Profile.name == "Tim OHagan"))
        tim_profile = result.scalars().first()
        
        if not tim_profile:
            tim_profile = Profile(
                name="Tim OHagan",
                bio="Forward Deployment Engineer deploying autonomous AI agent systems and self-healing cloud infrastructure into enterprise environments.",
                github_url="https://github.com/tmohagan"
            )
            session.add(tim_profile)
            await session.commit()
            await session.refresh(tim_profile)
            print(f"Created Profile: {tim_profile.name} (ID: {tim_profile.id})")
        else:
            tim_profile.bio = "Forward Deployment Engineer deploying autonomous AI agent systems and self-healing cloud infrastructure into enterprise environments."
            await session.commit()
            print(f"Updated Profile: {tim_profile.name} (ID: {tim_profile.id})")

        # Delete existing posts to replace with Forward Deployment posts
        await session.execute(delete(Post))
        await session.commit()
        print("Deleted existing posts to replace with Forward Deployment posts.")

        # Insert new Posts
        for post_info in POSTS_DATA:
            new_post = Post(
                title=post_info["title"],
                category=post_info.get("category", "Autonomous SRE"),
                content=post_info["content"],
                author_id=tim_profile.id
            )
            session.add(new_post)
            print(f"Added post: {post_info['title']} [{post_info.get('category')}]")
        
        await session.commit()
        print("Database seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed())
