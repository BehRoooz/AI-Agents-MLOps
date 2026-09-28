import os
import sys
sys.path.insert(0, 'src/aiops_agent_monitor')

from tools.mlops_tools import PrometheusQuery, LokiLogSearch, GrafanaDashboardLink

# Use localhost:9091 for local testing (matches docker-compose port mapping)
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9091")
os.environ["PROMETHEUS_URL"] = PROMETHEUS_URL

print(f"Using Prometheus URL: {PROMETHEUS_URL}")
print("=" * 60)

# Test 1: Query CPU metrics
print("\n=== Test 1: Query CPU Metrics ===")
result = PrometheusQuery.invoke({
    'query': 'rate(node_cpu_seconds_total{mode!="idle"}[5m])',
    'time_range_minutes': 15,
    'step_seconds': 30
})
print(result)

# Test 2: Invalid time range (should fail gracefully)
print("\n=== Test 2: Invalid Time Range (Expected Error) ===")
result = PrometheusQuery.invoke({
    'query': 'cpu_usage',
    'time_range_minutes': -10,  # Invalid!
    'step_seconds': 30
})
print(result)

# Test 3: Invalid step seconds (should fail gracefully)
print("\n=== Test 3: Invalid Step Seconds (Expected Error) ===")
result = PrometheusQuery.invoke({
    'query': 'up',
    'time_range_minutes': 5,
    'step_seconds': -5  # Invalid!
})
print(result)

print("\n" + "=" * 60)
print("Tests completed!")

# Test 4: Invalid step seconds (should fail gracefully)
print("\n===== Test 4: Invalid Step Seconds (Expected Error) =====")
result = PrometheusQuery.invoke({
    'query': 'rate(node_cpu_seconds_total{mode!="idle"}[5m])',
    'time_range_minutes': 15,
    'step_seconds': 5  # Invalid!
})
print(result)

# Test 5: Valid PromQL function (should pass)
print("\n===== Test 5: Valid PromQL Function (Expected Pass) =====")
result = PrometheusQuery.invoke({
    'query': 'rate(node_cpu_seconds_total[5m])', # 'rate' is allowed
    'time_range_minutes': 15,
    'step_seconds': 30
    })
print(result)

# Test 6: Invalid PromQL function (should fail gracefully)
print("\n===== Test 6: Invalid PromQL Function (Expected Error) =====")
result = PrometheusQuery.invoke({
    'query': 'dangerous_function(cpu_usage)',  # Not in whitelist,
    'time_range_minutes': 15,
    'step_seconds': 30
})
print(result)


# Test 7: LokiLogSearch
print("\n===== Test 7: LokiLogSearch =====")
result = LokiLogSearch.invoke({
    'query': '{job="docker"}',
    'time_range_minutes': 10,
    'limit': 5,
    'target_service': 'news-classifier-api'
})

print(result)

# Test 8: GrafanaDashboardLink
print("\n===== Test 8: GrafanaDashboardLink =====")
result = GrafanaDashboardLink.invoke({
    'dashboard_uid': 'news_classifier_health',
    'time_range_minutes': 60,
    'service_filter': 'news-classifier-api'
})
print(result)


print("\n" + "=" * 60)
print("Tests completed!")

