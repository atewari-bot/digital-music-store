from langgraph.checkpoint.memory import MemorySaver # For short-term memory
from langgraph.store.memory import InMemoryStore # For long-term memory
from typing import Dict, Any

# Shared instances to ensure all agents use the same store
_checkpointer = None
_store = None
_preferences_store: Dict[str, Any] = {}  # Simple dict for user preferences

def get_checkpointer() -> MemorySaver:
    """
    Returns a MemorySaver instance for short-term memory.

    This function creates and returns a MemorySaver instance that can be used to save and retrieve
    short-term memory in a LangGraph application.

    Returns:
        MemorySaver: An instance of MemorySaver for short-term memory.
    """
    global _checkpointer
    if _checkpointer is None:
        _checkpointer = MemorySaver()
    return _checkpointer

def get_in_memory_store() -> InMemoryStore:
    """
    Returns a shared InMemoryStore instance for long-term memory.

    This function creates and returns a shared InMemoryStore instance that can be used to store and retrieve
    long-term memory in a LangGraph application. All agents will share the same store instance.

    Returns:
        InMemoryStore: A shared instance of InMemoryStore for long-term memory.
    """
    global _store
    if _store is None:
        _store = InMemoryStore()
    return _store

def get_preferences_store() -> Dict[str, Any]:
    """
    Returns a simple dictionary for storing user preferences.
    
    This is a simple in-memory dict used for user preferences, separate from LangGraph's store.
    
    Returns:
        Dict: A shared dictionary for user preferences.
    """
    global _preferences_store
    return _preferences_store