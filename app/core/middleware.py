import os
import json
import traceback
import uuid
import asyncio
import httpx
from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

async def fire_webhook(payload: dict):
    """Isolated background coroutine to transmit telemetry over TCP."""
    webhook_url = os.environ.get("GHOSTMACHINE_WEBHOOK_URL", "http://ghostmachine.local:8000/api/webhooks")
    async with httpx.AsyncClient() as client:
        try:
            await client.post(webhook_url, json=payload, timeout=2.0)
        except Exception:
            pass # Silently fail if control plane is down

class GhostMachineMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract or generate OTel Trace ID from TCP headers
        trace_id = request.headers.get("x-b3-traceid") or uuid.uuid4().hex
        
        try:
            return await call_next(request)
        except Exception as exc:
            # 1. Capture RAM Stack Trace
            memory_trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            
            # 2. Extract TCP Socket Context
            fault_payload = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "trace_id": trace_id,
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "error_class": exc.__class__.__name__,
                "traceback": memory_trace
            }
            
            # 3. Append to Physical Disk Log
            log_path = "/var/log/ghostmachine/audit.log"
            try:
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, "a") as f:
                    f.write(json.dumps(fault_payload) + "\n")
            except Exception:
                pass
            
            # 4. Dispatch Asynchronous Network Signal
            asyncio.create_task(fire_webhook(fault_payload))
            
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "GhostMachine captured a critical fault.",
                    "trace_id": trace_id
                }
            )
