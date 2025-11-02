"""
Node to initialize state and extract customer ID from messages.
"""
from da.state import State
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from agents.customer_service.customer_service_agent import get_customer_id_from_identifier
from da.memory_utils import load_user_preferences
from typing import Tuple
import re
import logging


def extract_customer_id_from_messages(messages: list) -> Tuple[str, str]:
    """
    Extract customer ID from messages.
    
    Looks for customer ID patterns in messages and tries to resolve them.
    
    Args:
        messages: List of messages from the conversation.
        
    Returns:
        tuple: (customer_id as string, original_identifier if found)
    """
    if not messages:
        return "", ""
    
    # Look for customer ID patterns in messages
    patterns = [
        r"customer\s+id\s+is\s+(\d+)",
        r"customer\s+id:\s*(\d+)",
        r"customer\s+id\s*=\s*(\d+)",
        r"my\s+customer\s+id\s+is\s+(\d+)",
        r"customer\s+#\s*(\d+)",
        r"id\s+(\d+)",
    ]
    
    for message in messages:
        if isinstance(message, HumanMessage) and message.content:
            content = message.content.lower()
            
            # Try pattern matching
            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    customer_id = match.group(1)
                    logging.info(f"Found customer ID via pattern: {customer_id}")
                    return customer_id, customer_id
            
            # Try to find email or phone number
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message.content)
            phone_match = re.search(r'\+?\d{10,15}', message.content)
            
            if email_match:
                email = email_match.group(0)
                customer_id = get_customer_id_from_identifier(email)
                if customer_id:
                    logging.info(f"Found customer ID via email: {customer_id}")
                    return str(customer_id), email
            
            if phone_match:
                phone = phone_match.group(0)
                customer_id = get_customer_id_from_identifier(phone)
                if customer_id:
                    logging.info(f"Found customer ID via phone: {customer_id}")
                    return str(customer_id), phone
    
    return "", ""


def initialize_state(state: State, config: RunnableConfig) -> State:
    """
    Initialize state by extracting customer ID and loading user preferences.
    
    This node runs at the beginning of the workflow to:
    1. Extract customer ID from messages
    2. Load user preferences from memory
    3. Initialize state fields
    
    Args:
        state: The current state.
        config: Runnable config.
        
    Returns:
        State: Updated state with customer_id and loaded_memory.
    """
    # Extract customer ID if not already set
    customer_id = state.get("customer_id", "")
    if not customer_id or customer_id == "":
        customer_id, _ = extract_customer_id_from_messages(state.get("messages", []))
    
    # Load user preferences
    loaded_memory = "None"
    if customer_id and customer_id != "":
        loaded_memory = load_user_preferences(customer_id, config)
        logging.info(f"Initialized state for customer {customer_id}, loaded memory: {loaded_memory[:50] if len(loaded_memory) > 50 else loaded_memory}...")
    
    return {
        "customer_id": customer_id,
        "loaded_memory": loaded_memory,
        "messages": state.get("messages", []),
    }

