#!/usr/bin/env python3
import requests
r = requests.get("http://localhost:9090/api/v1/query", params={"query": 'sum(rate(istio_requests_total{destination_service="hello-world.default.svc.cluster.local"}[5m])) by (response_code, destination_version)'})

results = r.json()["data"]["result"]
version_a_200 = float([x for x in results if x["metric"]["destination_version"] == "v1" and x["metric"]["response_code"]=="200"][0]["value"][1])
version_a_500 = float([x for x in results if x["metric"]["destination_version"] == "v1" and x["metric"]["response_code"]=="500"][0]["value"][1])
version_a_total = version_a_200 + version_a_500

error_rate_a = version_a_500 / version_a_total
print("ERROR RATE:", error_rate_a)
