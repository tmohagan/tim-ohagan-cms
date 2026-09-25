from fastapi import FastAPI
from app.api.routes import profile, playground
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
app.include_router(playground.router, prefix="/playground", tags=["Chaos"])

@app.get("/health", tags=["System"])
async def health_check():
    """Deterministic pulse check to verify the process is alive."""
    return {"status": "ok", "service": "tim-ohagan-cms"}
