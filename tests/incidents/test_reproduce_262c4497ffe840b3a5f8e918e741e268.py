import httpx
import pytest


def test_reproduce_incident():
    base_url = "http://cms-app:8000"
    target_path = None
    target_method = "GET"

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        # Step 1: Discover route from OpenAPI schema if available
        for openapi_path in ["/openapi.json", "/api/v1/openapi.json", "/api/openapi.json"]:
            try:
                res = client.get(openapi_path)
                if res.status_code == 200:
                    spec = res.json()
                    paths = spec.get("paths", {})
                    for path, path_item in paths.items():
                        if not isinstance(path_item, dict):
                            continue
                        for method, op in path_item.items():
                            if not isinstance(op, dict):
                                continue
                            op_id = op.get("operationId", "")
                            if (
                                "trigger_cpu_500_error" in op_id
                                or "trigger_cpu_500_error" in path
                                or "trigger-cpu-500" in path
                                or ("playground" in path and "500" in path)
                            ):
                                target_path = path
                                target_method = method.upper()
                                break
                        if target_path:
                            break
            except Exception:
                pass
            if target_path:
                break

        # Step 2: If found in OpenAPI, send request to reproduce the 500 error
        if target_path:
            response = client.request(target_method, target_path)
            assert response.status_code == 500
            return

        # Step 3: Fallback candidates if OpenAPI discovery did not locate the endpoint
        candidates = [
            "/api/v1/playground/trigger-cpu-500-error",
            "/api/v1/playground/trigger_cpu_500_error",
            "/api/v1/playground/cpu-500-error",
            "/api/v1/playground/cpu-500",
            "/api/v1/playground/500",
            "/playground/trigger-cpu-500-error",
            "/playground/trigger_cpu_500_error",
            "/playground/cpu-500-error",
            "/playground/cpu-500",
            "/playground/500",
            "/api/playground/trigger-cpu-500-error",
            "/api/playground/trigger_cpu_500_error",
            "/api/playground/cpu-500",
            "/api/playground/500",
        ]

        for method in ["GET", "POST"]:
            for cand in candidates:
                try:
                    res = client.request(method, cand)
                    if res.status_code == 500:
                        assert res.status_code == 500
                        return
                except Exception:
                    pass

        # Final attempt to default path to assert status code 500
        fallback_path = "/api/v1/playground/trigger-cpu-500-error"
        response = client.get(fallback_path)
        assert response.status_code == 500