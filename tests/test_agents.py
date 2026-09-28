import sys
from pathlib import Path

import pytest
from langchain_core.messages import HumanMessage
from unittest.mock import MagicMock

# Ensure the project root is on sys.path before importing project modules
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.tools.mlops_tools import check_alert_severity
from src.agents.conditional_agent import create_alert_router_agent


def test_check_alert_severity():
    """Test the check_alert_severity function"""
    assert check_alert_severity("Database is DOWN") == "critical"
    assert check_alert_severity("CPU warning at 85%") == "medium"
    assert check_alert_severity("Disk space notification") == "low"


def test_alert_router_critical_path():
    """Test the critical alert path"""
    mock_llm = MagicMock(name="ChatGroqMock")
    graph = create_alert_router_agent(llm_client=mock_llm, tools_for_graph=[])

    result = graph.invoke({
        "messages": [HumanMessage(content="Production database is DOWN")],
        "alert_info": "Production database is DOWN",
        "alert_severity": "unknown",
        "investigation_query": "",
        "investigation_step": 0,
        "max_investigation_steps": 3,
        "log_found": False,
        "proposed_action": "",
        "human_approval_needed": False,
        "human_feedback": "",
        "system_metrics": {},
        "report_content": "",
        "final_result": ""
    })

    assert "CRITICAL" in result["final_result"]
    assert "escalation" in result["final_result"].lower()

def test_alert_router_medium_path():
    """Test the medium alert path."""
    mock_llm = MagicMock(name="ChatGroqMock")
    graph = create_alert_router_agent(llm_client=mock_llm, tools_for_graph=[])

    result = graph.invoke({
        "messages": [HumanMessage(content="CPU usage warning")],
        "alert_info": "CPU usage warning",
        "alert_severity": "unknown",
        "investigation_query": "",
        "investigation_step": 0,
        "max_investigation_steps": 3,
        "logs_found": False,
        "proposed_action": "",
        "human_approval_needed": False,
        "human_feedback": "",
        "system_metrics": {},
        "report_content": "",
        "final_result": ""
    })

    assert "MEDIUM" in result["final_result"]
    assert "diagnosis" in result["final_result"].lower()