#!/usr/bin/env python3
import requests
import sys

if len(sys.argv) != 3:
    print("Usage: check_status.py <version A> <version B>")
    sys.exit(1)

version_a = sys.argv[1]
version_b = sys.argv[2]

r = requests.get("http://localhost:9090/api/v1/query", params={"query": 'sum(rate(istio_requests_total{destination_service="hello-world.default.svc.cluster.local"}[1m])) by (response_code, destination_version)'})
results = r.json()["data"]["result"]

version_a_200 = float([x for x in results if x["metric"]["destination_version"] == version_a and x["metric"]["response_code"]=="200"][0]["value"][1])
version_a_total = sum([float(x["value"][1]) for x in results if x["metric"]["destination_version"] == version_a])
ok_rate_a = version_a_200 / version_a_total

version_b_200 = float([x for x in results if x["metric"]["destination_version"] == version_b and x["metric"]["response_code"]=="200"][0]["value"][1])
version_b_total = sum([float(x["value"][1]) for x in results if x["metric"]["destination_version"] == version_b])
ok_rate_b = version_b_200 / version_b_total

ok_percentage_a = int(ok_rate_a * 100 * 100) / 100
ok_percentage_b = int(ok_rate_b * 100 * 100) / 100

total_rate = version_a_total + version_b_total
serving_a_percentage = int((version_a_total / total_rate) * 100 * 100) / 100
serving_b_percentage = int((version_b_total / total_rate) * 100 * 100) / 100

print("OK RATE", version_a, "is", ok_percentage_a, "serving", serving_a_percentage)
print("OK RATE", version_b, "is", ok_percentage_b, "serving", serving_b_percentage)
