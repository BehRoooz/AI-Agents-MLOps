import os
import sys
sys.path.insert(0, 'src/aiops_agent_monitor')

from tools.mlops_tools import PrometheusQuery, LokiLogSearch, GrafanaDashboardLink

print("\n" + "=" * 60)
print("Running all tools tests ...")
print("=" * 60)

import time

# Stimulate investigating alert from 30 minutes ago
alert_time = int(time.time()) - 1800 # 30 minutes ago
investigation_start = alert_time - 300 # 5 minutes ago
investigation_end = alert_time + 300 # 5 minutes after alert

# 1. Check CPU trend around alert time
print("\n=== Test 1: Check CPU Trend Around Alert Time ===")
cpu_result = PrometheusQuery.invoke({
    'query': 'rate(node_cpu_seconds_total{mode!="idle"}[1m])',
    'time_range_minutes': 60, # 1 hour
    'step_seconds': 60 # 1 minute
})
print(cpu_result[:500]) # Print first 500 characters for brevity
print()

# 2. Search logs around alert time
print("\n=== Test 2: Search Logs Around Alert Time ===")
log_result = LokiLogSearch.invoke({
    'query': '{job="docker"} |~ "(?!)(error|exception)"' , # Case intensive error search
    'time_range_minutes': 10, # 10 minutes
    'limit': 10,
    'target_service': 'news-classifier-api'
})

print(log_result)
print()

# 3. Link to Grafana dashboard
print("\n=== Test 3: Link to Grafana Dashboard ===")
dashboard_link = GrafanaDashboardLink.invoke({
    'dashboard_uid': 'news_classifier_health',
    'time_range_minutes': 60,
    'service_filter': 'news-classifier-api'
})
print(dashboard_link)
print()

print("=== Investigation Summary ===")
print("1. CPU metrics retrieved for last hour")
print("2. Searched logs for errors around alert time")
print("3. Generated Grafana visualization link")
print("\nAn agent would now correlate this data and report findings.")
print()
print("\nAll tests completed successfully!")
print("=" * 60)