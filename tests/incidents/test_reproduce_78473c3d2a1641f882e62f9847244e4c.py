import httpx
import pytest


def test_reproduce_incident():
    base_url = "http://cms-app:8000"

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        target_path = None
        target_method = None

        # Inspect OpenAPI schema if available to find the exact route
        for openapi_path in ["/openapi.json", "/api/v1/openapi.json", "/api/openapi.json"]:
            try:
                resp = client.get(openapi_path)
                if resp.status_code == 200:
                    schema = resp.json()
                    paths = schema.get("paths", {})
                    for path, methods in paths.items():
                        for method, op in methods.items():
                            if isinstance(op, dict):
                                op_id = op.get("operationId", "")
                                if (
                                    "trigger_cpu_500" in op_id
                                    or "trigger_cpu_500" in path
                                    or "cpu-500" in path
                                    or "cpu_500" in op_id
                                ):
                                    target_path = path
                                    target_method = method.upper()
                                    break
                        if target_path:
                            break
                if target_path:
                    break
            except Exception:
                pass

        if target_path and target_method:
            response = client.request(target_method, target_path)
        else:
            candidates = [
                ("GET", "/api/v1/playground/trigger-cpu-500-error"),
                ("POST", "/api/v1/playground/trigger-cpu-500-error"),
                ("GET", "/playground/trigger-cpu-500-error"),
                ("POST", "/playground/trigger-cpu-500-error"),
                ("GET", "/api/v1/playground/trigger_cpu_500_error"),
                ("POST", "/api/v1/playground/trigger_cpu_500_error"),
                ("GET", "/playground/trigger_cpu_500_error"),
                ("POST", "/playground/trigger_cpu_500_error"),
                ("GET", "/api/v1/playground/cpu-500"),
                ("POST", "/api/v1/playground/cpu-500"),
                ("GET", "/playground/cpu-500"),
                ("POST", "/playground/cpu-500"),
            ]
            response = None
            for method, path in candidates:
                try:
                    res = client.request(method, path)
                    if res.status_code == 500:
                        response = res
                        break
                except Exception:
                    pass

            if response is None:
                response = client.get("/api/v1/playground/trigger-cpu-500-error")

        assert response.status_code == 500