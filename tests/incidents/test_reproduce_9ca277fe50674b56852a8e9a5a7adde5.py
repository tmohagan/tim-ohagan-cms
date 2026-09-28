import httpx
import pytest

def test_reproduce_incident():
    base_url = "http://cms-app:8000"
    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        target_path = None
        method = "GET"

        for openapi_path in ["/openapi.json", "/api/v1/openapi.json", "/api/openapi.json"]:
            try:
                resp = client.get(openapi_path)
                if resp.status_code == 200:
                    schema = resp.json()
                    for path, methods in schema.get("paths", {}).items():
                        for m, details in methods.items():
                            op_id = details.get("operationId", "")
                            if (
                                "trigger_cpu_500_error" in op_id
                                or "trigger_cpu_500_error" in path
                                or "cpu_500" in op_id
                                or "cpu-500" in path
                            ):
                                target_path = path
                                method = m.upper()
                                break
                        if target_path:
                            break
                if target_path:
                    break
            except Exception:
                pass

        if not target_path:
            candidates = [
                "/api/v1/playground/trigger-cpu-500-error",
                "/playground/trigger-cpu-500-error",
                "/api/v1/playground/trigger_cpu_500_error",
                "/playground/trigger_cpu_500_error",
                "/api/v1/playground/cpu-500-error",
                "/playground/cpu-500-error",
                "/api/v1/playground/cpu-500",
                "/playground/cpu-500",
                "/api/playground/trigger-cpu-500-error",
                "/trigger-cpu-500-error",
            ]
            for cand in candidates:
                for m in ["GET", "POST"]:
                    try:
                        r = client.request(m, cand)
                        if r.status_code == 500:
                            assert r.status_code == 500
                            return
                    except Exception:
                        pass
            target_path = candidates[0]

        response = client.request(method, target_path)
        assert response.status_code == 500