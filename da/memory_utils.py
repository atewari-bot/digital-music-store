"""
Memory utilities for saving and loading user preferences.

This module provides functions to interact with LangGraph's InMemoryStore
to save and load user preferences and other long-term memory data.
"""
from typing import Optional
from langchain_core.runnables import RunnableConfig
from da.memory import get_preferences_store
import logging


def load_user_preferences(customer_id: str, config: Optional[RunnableConfig] = None) -> str:
    """
    Load user preferences from the long-term memory store.
    
    Args:
        customer_id: The customer ID to load preferences for.
        config: Optional RunnableConfig (for future use if needed).
        
    Returns:
        str: The user preferences as a string, or "None" if not found.
    """
    if not customer_id or customer_id == "":
        return "None"
    
    try:
        store = get_preferences_store()
        key = f"customer_preferences:{customer_id}"
        
        # Simple dict access
        result = store.get(key)
        
        if result:
            logging.debug(f"Loaded preferences for customer {customer_id}: {result}")
            return str(result)
        else:
            logging.debug(f"No preferences found for customer {customer_id}")
            return "None"
    except Exception as e:
        logging.error(f"Error loading preferences for customer {customer_id}: {e}")
        return "None"


def save_user_preferences(customer_id: str, preferences: str, config: Optional[RunnableConfig] = None) -> bool:
    """
    Save user preferences to the long-term memory store.
    
    Args:
        customer_id: The customer ID to save preferences for.
        preferences: The preferences to save as a string.
        config: Optional RunnableConfig (for future use if needed).
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if not customer_id or customer_id == "":
        return False
    
    try:
        store = get_preferences_store()
        key = f"customer_preferences:{customer_id}"
        
        # Simple dict assignment
        store[key] = preferences
        logging.debug(f"Saved preferences for customer {customer_id}: {preferences}")
        return True
    except Exception as e:
        logging.error(f"Error saving preferences for customer {customer_id}: {e}")
        return False


def extract_preferences_from_messages(messages: list) -> Optional[str]:
    """
    Extract user preferences from conversation messages.
    
    This function looks through messages to identify preferences mentioned by the user.
    
    Args:
        messages: List of conversation messages.
        
    Returns:
        Optional[str]: Extracted preferences as a string, or None if no preferences found.
    """
    # This is a simple implementation. In a production system, you might use
    # an LLM to extract structured preferences from the conversation.
    preference_keywords = [
        "i like", "i prefer", "i love", "i enjoy", "my favorite",
        "i'm interested in", "i'm into", "i listen to"
    ]
    
    preferences = []
    for msg in messages:
        if hasattr(msg, 'content') and msg.content:
            content = msg.content.lower()
            for keyword in preference_keywords:
                if keyword in content:
                    # Extract a sentence or two around the preference
                    sentences = content.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            preferences.append(sentence.strip())
    
    if preferences:
        return "; ".join(preferences[:3])  # Limit to first 3 preferences
    return None

