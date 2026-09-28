import pytest
import httpx


def test_reproduce_incident():
    base_url = "http://cms-app:8000"
    target_path = None
    target_method = "GET"

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        # Discover the exact route from OpenAPI documentation if available
        for openapi_path in ["/openapi.json", "/api/v1/openapi.json", "/api/openapi.json"]:
            try:
                res = client.get(openapi_path)
                if res.status_code == 200:
                    schema = res.json()
                    paths = schema.get("paths", {})
                    for path, methods in paths.items():
                        for method, details in methods.items():
                            op_id = details.get("operationId", "")
                            summary = details.get("summary", "")
                            if (
                                "trigger_cpu_500_error" in op_id
                                or "trigger_cpu_500_error" in summary
                                or "trigger-cpu-500-error" in path
                                or "trigger_cpu_500_error" in path
                                or ("playground" in path and "cpu" in path)
                                or ("playground" in path and "500" in path)
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

        if target_path:
            response = client.request(target_method, target_path)
        else:
            # Candidate endpoints based on route file naming conventions
            candidates = [
                ("GET", "/playground/trigger-cpu-500-error"),
                ("POST", "/playground/trigger-cpu-500-error"),
                ("GET", "/playground/trigger_cpu_500_error"),
                ("POST", "/playground/trigger_cpu_500_error"),
                ("GET", "/playground/cpu-500"),
                ("POST", "/playground/cpu-500"),
                ("GET", "/playground/cpu-500-error"),
                ("POST", "/playground/cpu-500-error"),
                ("GET", "/api/v1/playground/trigger-cpu-500-error"),
                ("POST", "/api/v1/playground/trigger-cpu-500-error"),
                ("GET", "/api/v1/playground/trigger_cpu_500_error"),
                ("POST", "/api/v1/playground/trigger_cpu_500_error"),
                ("GET", "/api/v1/playground/cpu-500"),
                ("POST", "/api/v1/playground/cpu-500"),
                ("GET", "/api/playground/trigger-cpu-500-error"),
                ("POST", "/api/playground/trigger-cpu-500-error"),
                ("GET", "/trigger-cpu-500-error"),
                ("POST", "/trigger-cpu-500-error"),
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
                response = client.get("/playground/trigger-cpu-500-error")

        assert response.status_code == 500