import httpx
import pytest


def test_reproduce_incident():
    base_url = "http://cms-app:8000"
    target_url = None
    target_method = "GET"

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        for openapi_path in ["/openapi.json", "/api/v1/openapi.json", "/api/openapi.json"]:
            try:
                res = client.get(openapi_path)
                if res.status_code == 200:
                    data = res.json()
                    for path, methods in data.get("paths", {}).items():
                        for method, details in methods.items():
                            if not isinstance(details, dict):
                                continue
                            op_id = details.get("operationId", "")
                            summary = details.get("summary", "")
                            if (
                                "trigger_cpu_500_error" in op_id
                                or "trigger_cpu_500_error" in summary
                                or "trigger_cpu_500" in path
                                or "trigger-cpu-500" in path
                                or ("playground" in path and "500" in path)
                            ):
                                target_url = path
                                target_method = method.upper()
                                break
                        if target_url:
                            break
                if target_url:
                    break
            except Exception:
                pass

        if not target_url:
            target_url = "/api/v1/playground/trigger-cpu-500-error"

        response = None
        try:
            response = client.request(target_method, target_url)
        except Exception:
            pass

        if response is None or response.status_code != 500:
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
                ("GET", "/api/v1/playground/500"),
                ("POST", "/api/v1/playground/500"),
                ("GET", "/playground/500"),
                ("POST", "/playground/500"),
            ]
            for m, p in candidates:
                try:
                    r = client.request(m, p)
                    if r.status_code == 500:
                        response = r
                        break
                except Exception:
                    pass

        assert response is not None
        assert response.status_code == 500