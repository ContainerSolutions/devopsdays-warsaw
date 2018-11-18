#!/usr/bin/env python3
import requests

if len(sys.argv) != 2:
    print("Usage: check_status.py <version A> <version B>")
    os.exit(1)

version_a = sys.argv[0]
version_b = sys.argv[1]

r = requests.get("http://localhost:9090/api/v1/query", params={"query": 'sum(rate(istio_requests_total{destination_service="hello-world.default.svc.cluster.local"}[1m])) by (response_code, destination_version)'})
results = r.json()["data"]["result"]

version_a_200 = float([x for x in results if x["metric"]["destination_version"] == version_a and x["metric"]["response_code"]=="200"][0]["value"][1])
version_a_500 = float([x for x in results if x["metric"]["destination_version"] == version_a and x["metric"]["response_code"]=="500"][0]["value"][1])
version_a_total = version_a_200 + version_a_500
error_rate_a = version_a_500 / version_a_total

version_b_200 = float([x for x in results if x["metric"]["destination_version"] == version_b and x["metric"]["response_code"]=="200"][0]["value"][1])
version_b_500 = float([x for x in results if x["metric"]["destination_version"] == version_b and x["metric"]["response_code"]=="500"][0]["value"][1])
version_b_total = version_a_200 + version_a_500
error_rate_b = version_b_500 / version_b_total

print("ERROR RATE", version_a, "is", error_rate_a)
print("ERROR RATE", version_b, "is", error_rate_b)
