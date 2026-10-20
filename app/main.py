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

@app.get("/fa_demo", tags=["Frontend"])
@app.get("/fa_demo/", tags=["Frontend"], include_in_schema=False)
async def serve_franca_advisory_demo():
    """Serve the Franca Advisory website demo."""
    return FileResponse("app/static/fa_demo/index.html")

@app.get("/admin", tags=["Frontend"])
async def serve_admin(admin: str = Depends(get_current_admin)):
    """Serve the admin dashboard, protected by HTTP Basic Auth."""
    return FileResponse("app/static/admin.html")

from sqlalchemy.future import select
from sqlalchemy import delete
from seed_db import POSTS_DATA

@app.post("/seed", tags=["System"])
async def seed_production_db(
    db: AsyncSession = Depends(get_db),
    admin: str = Depends(get_current_admin)
):
    """Seed or update all showcase technical posts in the database. Protected by admin authentication."""
    bio_text = (
        "Forward Deployment & Agentic Engineer bridging executive brand, growth, and commercial strategy "
        "with production-grade AI agent systems and self-healing cloud infrastructure. Creator of GhostMachine.dev."
    )
    result = await db.execute(select(Profile).where(Profile.name == "Tim OHagan"))
    tim_profile = result.scalars().first()
    if not tim_profile:
        tim_profile = Profile(
            name="Tim OHagan",
            bio=bio_text,
            github_url="https://github.com/tmohagan"
        )
        db.add(tim_profile)
        await db.commit()
        await db.refresh(tim_profile)
    else:
        tim_profile.bio = bio_text
        await db.commit()

    # Clear existing posts to replace with Forward Deployment & Agentic Engineering posts
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
    return {"status": "success", "message": "All Forward Deployment & Agentic Engineering posts seeded successfully."}
