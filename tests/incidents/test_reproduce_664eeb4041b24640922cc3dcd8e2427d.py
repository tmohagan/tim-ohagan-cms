import httpx
import pytest

BASE_URL = "http://cms-app:8000"


def test_reproduce_incident():
    target_path = None
    target_method = "GET"

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # Attempt to discover the exact route from OpenAPI schema
        try:
            openapi_resp = client.get("/openapi.json")
            if openapi_resp.status_code == 200:
                schema = openapi_resp.json()
                for path, path_item in schema.get("paths", {}).items():
                    for method, operation in path_item.items():
                        if isinstance(operation, dict):
                            op_id = operation.get("operation_id", "")
                            if (
                                "trigger_cpu_500_error" in op_id
                                or "trigger_cpu_500_error" in path
                                or "cpu_500" in op_id
                                or "cpu-500" in path
                            ):
                                target_path = path
                                target_method = method.upper()
                                break
                    if target_path:
                        break
        except Exception:
            pass

        if target_path:
            response = client.request(target_method, target_path)
        else:
            candidate_routes = [
                ("GET", "/api/v1/playground/trigger-cpu-500-error"),
                ("POST", "/api/v1/playground/trigger-cpu-500-error"),
                ("GET", "/api/v1/playground/trigger_cpu_500_error"),
                ("POST", "/api/v1/playground/trigger_cpu_500_error"),
                ("GET", "/playground/trigger-cpu-500-error"),
                ("POST", "/playground/trigger-cpu-500-error"),
                ("GET", "/playground/trigger_cpu_500_error"),
                ("POST", "/playground/trigger_cpu_500_error"),
                ("GET", "/api/playground/trigger-cpu-500-error"),
                ("POST", "/api/playground/trigger-cpu-500-error"),
                ("GET", "/api/v1/playground/cpu-500"),
                ("POST", "/api/v1/playground/cpu-500"),
            ]
            response = None
            for method, path in candidate_routes:
                try:
                    resp = client.request(method, path)
                    if resp.status_code == 500:
                        response = resp
                        break
                    if resp.status_code != 404 and response is None:
                        response = resp
                except httpx.HTTPError:
                    continue

        assert response is not None, "Failed to reach target playground endpoint"
        assert response.status_code == 500