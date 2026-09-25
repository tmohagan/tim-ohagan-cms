from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import profile, playground, posts, comments
from app.core.middleware import GhostMachineMiddleware

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
