"""
State utility functions for initializing and managing agent state.
"""
from langchain_core.messages import HumanMessage
from agents.supervisor.nodes.initialize_state import extract_customer_id_from_messages
from da.memory_utils import load_user_preferences
import logging


def create_initial_state(message: str, customer_id: str = "", config=None) -> dict:
    """
    Create initial state for the agent.
    
    Args:
        message: The initial user message.
        customer_id: Optional customer ID (will be extracted from message if not provided).
        config: Optional RunnableConfig for loading preferences.
        
    Returns:
        dict: Initial state dictionary.
    """
    state = {
        "messages": [HumanMessage(content=message)],
        "customer_id": customer_id,
        "loaded_memory": "None",
    }
    
    # Extract customer ID if not provided
    if not customer_id or customer_id == "":
        extracted_id, _ = extract_customer_id_from_messages(state["messages"])
        if extracted_id:
            state["customer_id"] = extracted_id
            logging.info(f"Extracted customer ID: {extracted_id}")
    
    # Load preferences if customer ID is available
    if state["customer_id"] and state["customer_id"] != "":
        loaded_memory = load_user_preferences(state["customer_id"], config)
        state["loaded_memory"] = loaded_memory
        logging.info(f"Loaded memory for customer {state['customer_id']}")
    
    return state

