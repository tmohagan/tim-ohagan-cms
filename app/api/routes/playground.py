from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/fault/cpu-500", tags=["Chaos"])
@router.get("/fault/500", tags=["Chaos"])
async def trigger_cpu_500_error():
    """
    Intentionally triggers a divide-by-zero CPU fault to simulate an unhandled crash.
    Intercepted by GhostMachineMiddleware to trigger autonomous remediation.
    """
    fault = 1 / 0
    return {"result": fault}

@router.get("/fault/schema-422", tags=["Chaos"])
@router.get("/fault/422", tags=["Chaos"])
async def trigger_schema_422_error():
    """
    Simulates a malformed payload / schema validation error.
    """
    raise HTTPException(
        status_code=422, 
        detail="Simulated Schema Violation: Missing required telemetry schema field 'trace_id'"
    )

@router.get("/fault/db-deadlock", tags=["Chaos"])
async def trigger_db_deadlock():
    """
    Simulates a concurrent database transaction deadlock on row locks.
    Intercepted by GhostMachineMiddleware.
    """
    raise RuntimeError("Simulated DB Deadlock: Concurrent asyncpg update conflict on row lock 'profiles'")

@router.get("/fault/memory-asset", tags=["Chaos"])
async def trigger_memory_asset_exhaustion():
    """
    Simulates buffer allocation exhaustion / memory spike during asset processing.
    Intercepted by GhostMachineMiddleware.
    """
    raise MemoryError("Simulated Asset Exhaustion: Image buffer allocation exceeded 2048MB container memory limit")
