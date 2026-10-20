import asyncio
from app.core.database import AsyncSessionLocal
from app.models.sql_models import Profile, Post, Comment
from sqlalchemy.future import select
from sqlalchemy import delete

POSTS_DATA = [
    {
        "title": "The Last-Mile Advantage: How Forward Deployment Engineers Turn Advisory Strategy into Live AI Execution",
        "category": "Autonomous SRE",
        "content": """In modern consumer, brand, and business consulting, the bottleneck is rarely the quality of the strategy—it is the **last mile of execution**.

Executive leadership and advisory partners spend weeks crafting sharp commercial roadmaps: identifying market white space, redesigning operating models, and mapping high-ROI customer journeys. Yet when those strategies are handed off as slide decks, momentum stalls in months-long internal IT queues or fragmented vendor handoffs.

As a **Forward Deployment Engineer (FDE)** and Agentic Engineer, I sit directly at the intersection of strategic advisory and production software engineering:

1. **From Strategy Deck to Deployed Agent Workflow**: Embedding directly alongside strategy leads and client stakeholders to turn brand, content, and growth playbooks into working, production-grade LangGraph systems in days rather than quarters.
2. **Proof Over Positioning**: Informed clients and modern consumers expect empirical proof, not just positioning. Shipping live AI prototypes, interactive evaluation harnesses, and automated ROI ledgers transforms strategic recommendations into tangible, proprietary client capabilities.
3. **Self-Healing Production Resilience (`GhostMachine.dev`)**: Ensuring that every client-facing application, digital campaign, and data pipeline is backed by autonomous Site Reliability Engineering that detects and repairs faults in real time."""
    },
    {
        "title": "Winning the Agentic Shelf: Forward-Deploying AI Discovery & MCP Systems for Consumer Brands",
        "category": "Agentic Architecture",
        "content": """Consumer packaged goods (CPG), food & beverage, and retail brands are navigating a structural shift: private-label competition is intensifying, shoppers are demanding clean-label transparency, and **AI agents are rapidly disrupting how consumers discover, evaluate, and purchase products**.

When shoppers rely on AI assistants and autonomous shopping agents to curate their baskets, compare nutritional profiles, or find emerging brands, traditional SEO and static shelf placement are no longer enough. Forward Deployment Engineering enables brands to win the **Agentic Shelf**:

1. **Model Context Protocol (MCP) Brand Endpoints**:
I architect and deploy standardized MCP servers that expose machine-verified brand data—ingredient transparency, functional health attributes, real-time inventory, and promotional offers—directly to AI shopping and discovery agents.

2. **Autonomous White-Space & Category Intelligence**:
Using stateful LangGraph pipelines, I build multi-agent research systems that continuously ingest syndicated retail velocity signals, shopper sentiment, and competitive shifts—synthesizing real-time white-space opportunities for brand and commercial teams.

3. **Omnichannel Content & Activation Engines**:
Agentic workflows that adapt core brand positioning and creative strategy across retail media networks, shopper marketing channels, and conversational interfaces while preserving strict brand equity."""
    },
    {
        "title": "Protecting High-Stakes Brand Activations with GhostMachine.dev: Zero-Downtime SRE for Viral Campaigns",
        "category": "Autonomous SRE",
        "content": """Breakthrough marketing campaigns, national QSR promotions, and viral product drops are designed to generate massive, sudden surges in consumer traffic. Yet nothing destroys the ROI of a multimillion-dollar media buy faster than a `500 Internal Server Error` or checkout database deadlock at the exact moment consumer attention peaks.

I built **GhostMachine.dev**—and embedded the interactive **Break My Site** and **Chaos Playground** features right on this site—to prove how autonomous Site Reliability Engineering protects high-visibility digital experiences:

• **Instant Fault Interception**: `GhostMachineMiddleware` monitors live web applications and APIs at the network boundary, capturing unhandled exceptions and OpenTelemetry trace context (`x-b3-traceid`) the millisecond a traffic surge triggers a failure.
• **52-Second Autonomous Remediation**: Instead of waiting 45 to 60 minutes for an on-call engineer to wake up, dig through logs, and push a hotfix while paid media traffic bounces, GhostMachine synthesizes a `pytest` reproduction test, verifies a code patch in an isolated sandbox, and opens a verified GitHub Pull Request in **~52 seconds**.
• **99.94% Incident Cost Reduction**: Slashes tier-1 incident resolution from ~$42.50 in manual engineering labor to **$0.0263** in Gemini Flash inference and sandbox compute—protecting both campaign conversion rates and operating margins."""
    },
    {
        "title": "Brand Safety & Compliance by Compiler: Zero-Trust AST Guardrails for Enterprise AI",
        "category": "AI Security & Guardrails",
        "content": """For iconic heritage brands and fast-scaling consumer companies alike, brand equity and consumer trust are non-negotiable. Marketing and technology leaders rightly hesitate to deploy autonomous AI agents when safety relies on fragile prompt instructions ("Please stay on brand and never expose customer data").

As an Agentic and Forward Deployment Engineer, I replace prompt-level wishful thinking with **deterministic, compiler-level guardrails**:

1. **Abstract Syntax Tree (AST) Static Verification**:
In `GhostMachine.dev`, every AI-generated patch is parsed into an in-memory syntax tree using Python's native `ast` compiler before touching disk. Our `SecurityAuditVisitor` mathematically blocks dangerous system calls (`os.system`, `subprocess`, `eval`) and silent error suppression (bare `except:` blocks).

2. **Boundary PII & Secret Redaction**:
Consumer and commercial stacks process sensitive first-party loyalty, CRM, and partner credentials. Our telemetry layer automatically scrubs `Authorization`, `Cookie`, and API key headers at the ingress boundary before any payload enters an LLM context window.

3. **Surgical Scope Constraints**:
Automated diffs and workflow actions are hard-capped and validated against strict Pydantic schemas, ensuring deployed AI agents operate with zero-trust safety and full enterprise compliance."""
    },
    {
        "title": "Pre-Launch Battle Testing: Synthetic Chaos Engineering in the Chaos Playground",
        "category": "Chaos Engineering",
        "content": """In commercial and digital transformation, the difference between a category-defining launch and a public outage comes down to pre-launch operational readiness. Before a brand commits major budget to a national campaign, retail media blitz, or omnichannel partnership, its digital infrastructure must be proven under stress.

The interactive **Chaos Playground** (`/#playground`) on this portfolio demonstrates how I use **Synthetic Chaos Engineering** to harden client systems before launch day:

1. **CPU & Runtime Fault Injection (`/fault/cpu-500`)**: Simulates unhandled application crashes under peak promotional load to verify real-time telemetry capture and automated patch synthesis.
2. **Martech & API Schema Drift (`/fault/schema-422`)**: Simulates malformed payloads across CRM, CDP, and commerce webhooks, ensuring agents synthesize resilient validation fallbacks rather than dropping customer transactions.
3. **High-Concurrency Database Deadlocks (`/fault/db-deadlock`)**: Simulates concurrent `asyncpg` row-lock contention during flash sales or limited-edition drops, validating automated connection-pool backoff and recovery.
4. **Media Asset & Memory Exhaustion (`/fault/memory-asset`)**: Tests high-resolution creative and streaming backpressure so campaign experiences remain fast and resilient on every device."""
    },
    {
        "title": "From Consumer Insight to Execution: Multi-Agent LangGraph Pipelines for Growth & Content Operations",
        "category": "Agentic Architecture",
        "content": """Strategic consulting and modern growth marketing span multiple disciplines: consumer insight synthesis, brand positioning, content strategy, and commercial execution. A massive lever for advisory teams and enterprise growth orgs is transforming repetitive analysis and content adaptation cycles into scalable, high-margin agentic software.

Using **LangGraph** stateful orchestration, I design multi-agent pipelines built for commercial and creative velocity:

• **Specialized Subagent Handshakes**: Instead of monolithic prompts that degrade over long contexts, workflows are partitioned across specialized agents—an *Insight & Trend Analyst* (synthesizing category and shopper data), a *Positioning & Equity Filter* (evaluating opportunities against brand guardrails), and an *Activation Architect* (drafting channel-specific briefs and assets).
• **Human-in-the-Loop (HITL) Executive Checkpoints**: Backed by PostgreSQL state persistence (`PostgresSaver`), workflows automatically pause at critical decision nodes—allowing strategy leads and client executives to review, refine, and approve outputs before downstream execution proceeds.
• **Reusable Technical Leverage**: Every forward-deployed pipeline becomes a repeatable, proprietary asset that accelerates delivery across client engagements."""
    },
    {
        "title": "Hermetic Multi-Tenant Sandboxes: Protecting Proprietary Client Data with Docker & gVisor (`runsc`)",
        "category": "Chaos Engineering",
        "content": """When deploying AI agents and analytics workflows across multiple client organizations—each with confidential product roadmaps, pricing elasticity models, and commercial data—strict tenant isolation is mandatory. Standard container runtimes share the host OS kernel, leaving a potential surface for cross-workload interference.

To deliver zero-trust isolation in `GhostMachine.dev` and client deployments, I architect execution sandboxes using Google's **gVisor (`runsc`)** user-space kernel:

1. **User-Space Syscall Interception**: gVisor implements an independent Linux kernel in Go that intercepts all application system calls in user space, preventing untrusted or AI-generated code from ever interacting directly with the host kernel.
2. **Deterministic Resource Ceilings**: Every sandbox container is locked to an isolated bridge network with hard memory (`2048 MB`) and CPU (`2 vCPU`) limits, preventing resource contention or runaway processes.
3. **Ephemeral Zero-Retention Execution**: Containers spin up on demand for a single verification or analytics task and are immediately destroyed (`remove=True`), giving enterprise stakeholders complete confidence in data and IP security."""
    },
    {
        "title": "Proof Over Positioning: OpenTelemetry & Economic Ledgers that Quantify Client ROI",
        "category": "AI Security & Guardrails",
        "content": """The most effective brand, growth, and transformation initiatives are defined by measurable business results—work that builds both brand equity and the bottom line. When executives invest in AI transformation, they expect transparent, auditable proof of effectiveness rather than abstract technical metrics.

In every Forward Deployment Engineering engagement—and natively inside `GhostMachine.dev`—I build an **Economic Telemetry Ledger** directly into the OpenTelemetry pipeline:

• **Unit-Economic Attribution**: Every automated workflow and self-healing pull request calculates its own real-time ROI—comparing exact LLM token consumption and container compute seconds (`$0.0263`) against manual baseline labor costs (`~$42.50`).
• **End-to-End Traceability**: Distributed `x-b3-traceid` identifiers link every agent action, tool call, and sandbox verification run directly to operational and commercial KPIs (uptime during campaign peaks, speed-to-market, and hours saved).
• **Executive-Ready Reporting**: Delivers clear, boardroom-ready telemetry that proves how deployed AI agents drive sustainable business growth."""
    }
]

async def seed():
    async with AsyncSessionLocal() as session:
        # Check or Create Profile
        result = await session.execute(select(Profile).where(Profile.name == "Tim OHagan"))
        tim_profile = result.scalars().first()
        
        bio_text = (
            "Forward Deployment & Agentic Engineer bridging executive brand, growth, and commercial strategy "
            "with production-grade AI agent systems and self-healing cloud infrastructure. Creator of GhostMachine.dev."
        )

        if not tim_profile:
            tim_profile = Profile(
                name="Tim OHagan",
                bio=bio_text,
                github_url="https://github.com/tmohagan"
            )
            session.add(tim_profile)
            await session.commit()
            await session.refresh(tim_profile)
            print(f"Created Profile: {tim_profile.name} (ID: {tim_profile.id})")
        else:
            tim_profile.bio = bio_text
            await session.commit()
            print(f"Updated Profile: {tim_profile.name} (ID: {tim_profile.id})")

        # Delete existing posts to replace with Forward Deployment & Agentic Engineering posts
        await session.execute(delete(Post))
        await session.commit()
        print("Deleted existing posts to replace with Forward Deployment & Agentic Engineering posts.")

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
