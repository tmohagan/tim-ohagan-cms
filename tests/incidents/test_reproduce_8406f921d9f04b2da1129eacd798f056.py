import httpx
import pytest


def test_reproduce_incident():
    base_url = "http://cms-app:8000"
    target_path = None
    target_method = "GET"

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        # Dynamically discover the route path from OpenAPI schema if available
        try:
            openapi_resp = client.get("/openapi.json")
            if openapi_resp.status_code == 200:
                schema = openapi_resp.json()
                paths = schema.get("paths", {})
                for path, methods in paths.items():
                    for method, details in methods.items():
                        if isinstance(details, dict):
                            op_id = details.get("operationId", "")
                            summary = details.get("summary", "")
                            description = details.get("description", "")
                            info_str = f"{op_id} {summary} {description} {path}"
                            if "trigger_cpu_500_error" in info_str:
                                target_path = path
                                target_method = method.upper()
                                break
                            elif "playground" in path and ("cpu" in path or "500" in path):
                                target_path = path
                                target_method = method.upper()
                    if target_path and "trigger_cpu_500_error" in info_str:
                        break
        except Exception:
            pass

        # Fallback candidate endpoints if not discovered via OpenAPI
        if not target_path:
            candidates = [
                ("GET", "/api/v1/playground/trigger-cpu-500-error"),
                ("GET", "/api/v1/playground/cpu-500"),
                ("GET", "/api/v1/playground/cpu-500-error"),
                ("GET", "/playground/trigger-cpu-500-error"),
                ("GET", "/playground/cpu-500"),
                ("GET", "/playground/cpu-500-error"),
                ("POST", "/api/v1/playground/trigger-cpu-500-error"),
                ("POST", "/playground/trigger-cpu-500-error"),
            ]
            for method, path in candidates:
                try:
                    resp = client.request(method, path)
                    if resp.status_code == 500:
                        target_path = path
                        target_method = method
                        assert resp.status_code == 500
                        return
                except Exception:
                    pass

            target_path = "/api/v1/playground/trigger-cpu-500-error"
            target_method = "GET"

        response = client.request(target_method, target_path)
        assert response.status_code == 500