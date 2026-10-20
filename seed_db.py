import asyncio
from app.core.database import AsyncSessionLocal
from app.models.sql_models import Profile, Post, Comment
from sqlalchemy.future import select
from sqlalchemy import delete

POSTS_DATA = [
    {
        "title": "Why Brand & Growth Advisories Need a Forward Deployment Engineer: A Blueprint for The Franca Advisory",
        "category": "Autonomous SRE",
        "content": """Franci Lencioni founded **The Franca Advisory** on a rare executive perspective: seeing the consumer business from more than one side of the table—spanning high-growth CPG brand management at Nature's Path to Effie-, WARC Effective 100-, and Fast Company-winning marketing innovation at McDonald's USA.

In today's consumer landscape, however, there is a critical third side of the table: **autonomous technical execution**.

Traditional brand and marketing consultancies deliver brilliant strategy decks—identifying consumer white space, brand positioning, and commercial operating models—only to watch execution stall for months in client IT queues. By embedding a **Forward Deployment Engineer (FDE)** directly into The Franca Advisory's engagements, strategic vision becomes deployed reality within days:

1. **From Brand Strategy to Live Agent Workflows**: Translating Franca Advisory's growth marketing and content strategies into custom, production-grade LangGraph agent pipelines deployed directly inside client cloud environments.
2. **Proof Over Positioning**: Modern shoppers and enterprise CMOs alike expect empirical proof, not just positioning. Pairing strategic advisory with live engineering prototypes and automated ROI ledgers gives Franca Advisory an unassailable competitive moat.
3. **Self-Healing Client Infrastructure (`GhostMachine.dev`)**: Guaranteeing that the digital storefronts, promotional microsites, and data pipelines powering client brand activations remain 100% resilient under peak traffic."""
    },
    {
        "title": "Winning the Agentic Shelf: Forward-Deploying AI Discovery Systems for CPG & Consumer Brands",
        "category": "Agentic Architecture",
        "content": """CPG and retail marketing are undergoing a structural reckoning: private-label brands are scaling rapidly, consumer nutritional preferences are shifting toward clean-label transparency, and **AI agents are disrupting how shoppers discover, compare, and purchase products**.

When consumers ask AI assistants to build their grocery baskets or recommend functional food and beverage brands, traditional SEO and shelf placement are no longer enough. For **The Franca Advisory's** CPG and retail clients, I forward-deploy the technical infrastructure required to win the **Agentic Shelf**:

1. **Model Context Protocol (MCP) Brand Endpoints**:
We expose structured, machine-verified product attributes—clean-label ingredients, protein-to-fiber ratios, sustainability proofs, and real-time retail availability—directly to AI shopping agents via standardized MCP servers.

2. **Autonomous White-Space & Trend Radar**:
Using stateful LangGraph pipelines, we continuously synthesize syndicated retail velocity signals, consumer sentiment, and emerging category shifts into actionable white-space briefs for Franca Advisory's strategy leads.

3. **Dynamic Omnichannel Content Engines**:
Multi-agent workflows that adapt core brand equity and campaign messaging across retail media networks, shopper marketing touchpoints, and conversational commerce interfaces without diluting brand voice."""
    },
    {
        "title": "Protecting High-Stakes Brand Activations with GhostMachine.dev: Zero-Downtime SRE for Viral Campaigns",
        "category": "Autonomous SRE",
        "content": """Iconic consumer campaigns—like the Gold Effie and Ad Age Marketer of the Year activations Franci Lencioni helped spearhead at McDonald's—generate massive, sudden surges in digital traffic. When a youth marketing drop, loyalty app partnership, or national QSR promotion goes viral, a single unhandled `500` error or database deadlock burns millions in media spend and erodes hard-won brand equity.

I built **GhostMachine.dev** to serve as an autonomous Site Reliability Engineering (SRE) shield for mission-critical digital experiences:

• **Real-Time Fault Interception**: `GhostMachineMiddleware` monitors client web apps and APIs at the network boundary, capturing unhandled exceptions and OpenTelemetry trace context (`x-b3-traceid`) the millisecond a campaign spike triggers a fault.
• **52-Second Autonomous Remediation**: Instead of waiting 45+ minutes for an on-call contractor to wake up and debug logs while paid media traffic bounces, GhostMachine synthesizes a `pytest` reproduction test, verifies the fix in a sandbox, and opens a verified GitHub Pull Request in **~52 seconds**.
• **99.94% Incident Cost Reduction**: Reduces tier-1 campaign incident resolution from ~$42.50 in manual engineering labor to **$0.0263** in Gemini Flash inference and sandbox compute—protecting both campaign conversion rates and client margins."""
    },
    {
        "title": "Brand Safety by Compiler, Not Prompt: Zero-Trust AST Guardrails for Enterprise Marketing AI",
        "category": "AI Security & Guardrails",
        "content": """When advising heritage consumer brands and scaling CPG leaders, brand equity and consumer trust are sacred. CMOs and enterprise InfoSec teams rightly hesitate to deploy generative AI agents if those systems rely solely on fragile prompt instructions ("Please stay on brand and do not leak customer data").

As a Forward Deployment Engineer for **The Franca Advisory**, I replace prompt-level wishful thinking with **deterministic, compiler-level guardrails**:

1. **Abstract Syntax Tree (AST) Static Verification**:
In `GhostMachine.dev`, every line of AI-synthesized code is parsed through Python's native `ast` compiler via a custom `SecurityAuditVisitor`. Dangerous primitives (`os.system`, `subprocess`, `eval`) and silent failure patterns (bare `except:` blocks) are mathematically rejected before execution.

2. **Boundary PII & Credential Redaction**:
Consumer marketing stacks handle sensitive first-party loyalty and CRM data. Our telemetry middleware automatically scrubs `Authorization`, `Cookie`, and API key headers at the ingress boundary before any payload reaches an LLM context window.

3. **Surgical Scope Constraints**:
Automated patches and workflow mutations are hard-capped and gated behind deterministic validation, ensuring AI agents act as disciplined force multipliers that never compromise brand safety or regulatory compliance."""
    },
    {
        "title": "Stress-Testing Campaign Launches: Synthetic Chaos Engineering Before the Media Drop",
        "category": "Chaos Engineering",
        "content": """In consumer brand consulting, the difference between a breakthrough product launch and a digital misfire comes down to operational readiness. Before a client of **The Franca Advisory** commits millions to a national media buy, retail media push, or high-profile brand partnership, their digital commerce and fulfillment stack must be battle-tested.

Using the **Chaos Playground** architecture built into this portfolio and `GhostMachine.dev`, I bring proactive **Synthetic Chaos Engineering** to client launches:

1. **Traffic Spike & CPU Fault Simulation (`/fault/cpu-500`)**: Validates that unhandled runtime exceptions under promotional load are immediately intercepted and routed to autonomous remediation.
2. **Martech & Payload Schema Drift (`/fault/schema-422`)**: Simulates breaking API changes across CRM, CDP, and checkout webhooks so agents can synthesize resilient Pydantic fallback schemas ahead of launch.
3. **High-Concurrency Checkout Deadlocks (`/fault/db-deadlock`)**: Simulates database row-lock contention during flash sales or limited-edition drops, verifying connection-pool backoff and recovery.
4. **Media Asset & Memory Exhaustion (`/fault/memory-asset`)**: Tests high-resolution creative and video streaming backpressure so campaign landing pages stay fast and responsive on every device."""
    },
    {
        "title": "From Consumer Insight to Execution: Multi-Agent LangGraph Pipelines for Content & Growth Strategy",
        "category": "Agentic Architecture",
        "content": """**The Franca Advisory** operates across Brand Marketing, Content Strategy, Growth Marketing, and Business Consulting. A major opportunity for modern advisory practices is turning labor-intensive research and content adaptation cycles into repeatable, high-margin software assets.

Using **LangGraph** stateful orchestration, I architect multi-agent systems tailored to advisory workflows:

• **Specialized Subagent Handshakes**: Rather than a single monolithic prompt that suffers from context drift, we partition workflows across specialized agents—a *Consumer Insight Analyst* (parsing category and shopper trends), a *Brand Strategy Architect* (filtering opportunities through brand equity and stretch), and a *Content Execution Agent* (generating channel-ready creative briefs).
• **Human-in-the-Loop (HITL) Executive Checkpoints**: Powered by durable PostgreSQL state persistence (`PostgresSaver`), agent workflows automatically pause at critical decision nodes—allowing Franci and client stakeholders to review, steer, and approve strategic outputs before downstream execution proceeds.
• **Repeatable Advisory IP**: Every forward-deployed workflow becomes reusable, proprietary technical leverage that scales The Franca Advisory's impact across engagements."""
    },
    {
        "title": "Hermetic gVisor Sandboxes: Running Proprietary Brand & Commercial Analytics with Zero Data Leakage",
        "category": "Chaos Engineering",
        "content": """Advisory firms working across the food, beverage, CPG, and QSR ecosystems handle highly confidential commercial data: unannounced product innovación pipelines, pricing elasticity models, and retail distribution agreements. Running AI agents or automated code synthesis across multi-tenant client environments requires absolute isolation.

In `GhostMachine.dev`, I engineered our execution environment around Google's **gVisor (`runsc`)** user-space kernel to guarantee enterprise-grade tenant isolation:

1. **Kernel-Level Syscall Interception**: Every AI-generated test or analytics script executes inside an ephemeral Docker container isolated by `runsc`, intercepting system calls in user space so untrusted code never touches the host kernel.
2. **Strict Resource & Network Ceilings**: Sandboxes are locked to dedicated bridge networks and bounded by hard CPU (`2 vCPU`) and memory (`2048 MB`) limits, eliminating cross-client data bleed or runaway compute.
3. **Ephemeral Lifecycle**: Containers are provisioned on demand for a single verification run and immediately destroyed (`remove=True`), giving The Franca Advisory's enterprise clients bank-grade confidence in how their proprietary data and code are handled."""
    },
    {
        "title": "Proving Effectiveness on the Balance Sheet: OpenTelemetry & Economic Ledgers for Advisory ROI",
        "category": "AI Security & Guardrails",
        "content": """Throughout Franci Lencioni's career—highlighted by three consecutive #1 rankings on the **WARC Effective 100** and multiple **Gold Effie Awards**—the defining hallmark of her work has been *effectiveness*: creative, strategic work that measurably builds both the brand and the business.

When forward-deploying AI agents and autonomous infrastructure for **The Franca Advisory**, I build that same obsession with measurable effectiveness directly into the telemetry layer:

• **Automated Economic Telemetry Ledgers**: Every autonomous workflow and GhostMachine pull request calculates its own unit economics in real time—tracking exact LLM token consumption, container compute seconds, cycle-time compression, and net dollar savings against manual baseline costs.
• **End-to-End OpenTelemetry Attribution**: Distributed trace IDs connect technical execution metrics (uptime, latency, autonomous fault recovery) directly to commercial outcomes (campaign conversion continuity, shopper engagement, and speed-to-market).
• **Boardroom-Ready Reporting**: Gives Franca Advisory and its client CMOs/CEOs transparent, auditable proof of how AI transformation translates into bottom-line growth."""
    }
]

async def seed():
    async with AsyncSessionLocal() as session:
        # Check or Create Profile
        result = await session.execute(select(Profile).where(Profile.name == "Tim OHagan"))
        tim_profile = result.scalars().first()
        
        bio_text = (
            "Forward Deployment Engineer & creator of GhostMachine.dev—partnering with executive brand and growth "
            "leaders like The Franca Advisory to turn consumer strategy into deployed, production-grade AI agent systems."
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

        # Delete existing posts to replace with Franca Advisory & Forward Deployment posts
        await session.execute(delete(Post))
        await session.commit()
        print("Deleted existing posts to replace with Franca Advisory & Forward Deployment posts.")

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
