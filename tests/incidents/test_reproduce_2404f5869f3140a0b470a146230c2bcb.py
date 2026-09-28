import httpx
import pytest

def test_reproduce_incident():
    base_url = "http://cms-app:8000"
    target_method = "GET"
    target_path = None

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        # Attempt discovery via OpenAPI schema
        for openapi_path in ["/openapi.json", "/api/v1/openapi.json", "/api/openapi.json"]:
            try:
                resp = client.get(openapi_path)
                if resp.status_code == 200:
                    schema = resp.json()
                    paths = schema.get("paths", {})
                    for path, methods in paths.items():
                        for method, details in methods.items():
                            op_id = details.get("operationId", "").lower()
                            summary = details.get("summary", "").lower()
                            path_lower = path.lower()
                            if (
                                "trigger_cpu_500_error" in op_id
                                or "cpu_500" in op_id
                                or "cpu_500" in path_lower
                                or "trigger_cpu_500" in path_lower
                                or "cpu_500" in summary
                            ):
                                target_method = method.upper()
                                target_path = path
                                break
                        if target_path:
                            break
                if target_path:
                    break
            except Exception:
                pass

        # Fallback candidate routes if schema lookup is unavailable
        if not target_path:
            candidates = [
                "/api/v1/playground/cpu-500",
                "/api/v1/playground/trigger-cpu-500-error",
                "/api/v1/playground/error-500",
                "/playground/cpu-500",
                "/playground/trigger-cpu-500-error",
                "/playground/error-500",
                "/api/playground/cpu-500",
                "/api/playground/trigger-cpu-500-error",
            ]
            for path in candidates:
                for method in ["GET", "POST"]:
                    try:
                        resp = client.request(method, path)
                        if resp.status_code == 500:
                            target_path = path
                            target_method = method
                            break
                    except Exception:
                        pass
                if target_path:
                    break

        assert target_path is not None, "Failed to resolve endpoint for trigger_cpu_500_error"

        response = client.request(target_method, target_path)
        assert response.status_code == 500