import logging

from langchain_core.messages import AIMessage

from src.state import AgentState

logger = logging.getLogger(__name__)


def handle_urgent_alert_node(state: AgentState):
    logger.info(f"Node 'handle_urgent_alert': Urgent alert ({state['alert_info']}). Launching manual intervention.")
    final_msg = "URGENT alert detected. Launching manual intervention."
    return {"messages": [AIMessage(content=final_msg)], "final_result": final_msg}