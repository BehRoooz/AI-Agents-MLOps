import os
import sys
from pathlib import Path

# Ensure aiops_agent_monitor is importable (tools package lives there)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AIOPS_ROOT = PROJECT_ROOT / "src" / "aiops_agent_monitor"
if str(AIOPS_ROOT) not in sys.path:
    sys.path.insert(0, str(AIOPS_ROOT))

# Use localhost:9091 for local testing (matches docker compose port mapping)
os.environ.setdefault("PROMETHEUS_URL", "http://localhost:9091")

from tools.mlops_tools import PrometheusQuery


def test_prometheus_query_cpu_metrics():
    """Fetch CPU metrics from Prometheus with a valid PromQL range query."""
    result = PrometheusQuery.invoke({
        "query": 'rate(node_cpu_seconds_total{mode!="idle"}[5m])',
        "time_range_minutes": 15,
        "step_seconds": 30,
    })

    assert isinstance(result, str)
    assert "Prometheus query results:" in result
    assert "values:" in result
    assert "Failed to query Prometheus" not in result
    assert "unexpected error" not in result.lower()


def test_prometheus_query_invalid_time_range():
    """Negative time_range_minutes should fail gracefully."""
    result = PrometheusQuery.invoke({
        "query": "cpu_usage",
        "time_range_minutes": -10,
        "step_seconds": 30,
    })

    assert isinstance(result, str)
    assert "time_range_minutes must be positive" in result
    assert "An unexpected error occurred" in result


def test_prometheus_query_invalid_step_seconds():
    """Negative step_seconds should fail gracefully."""
    result = PrometheusQuery.invoke({
        "query": "up",
        "time_range_minutes": 5,
        "step_seconds": -5,
    })

    assert isinstance(result, str)
    assert "step_seconds must be positive" in result
    assert "An unexpected error occurred" in result
