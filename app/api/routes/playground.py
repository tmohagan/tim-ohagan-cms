from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/fault/500", tags=["Chaos"])
async def trigger_500_error():
    """Intentionally triggers a divide-by-zero CPU fault to simulate an unhandled exception."""
    # This halts the call stack and forces an exception in the Python runtime
    fault = 1 / 0
    return {"result": fault}

@router.get("/fault/422", tags=["Chaos"])
async def trigger_422_error():
    """Simulates a malformed byte payload by raising a physical validation error."""
    raise HTTPException(status_code=422, detail="Simulated Unprocessable Entity")
