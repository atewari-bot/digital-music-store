from langgraph.checkpoint.memory import MemorySaver # For short-term memory
from langgraph.store.memory import InMemoryStore # For long-term memory

def get_checkpointer() -> MemorySaver:
    """
    Returns a MemorySaver instance for short-term memory.

    This function creates and returns a MemorySaver instance that can be used to save and retrieve
    short-term memory in a LangGraph application.

    Returns:
        MemorySaver: An instance of MemorySaver for short-term memory.
    """
    checkpointer = MemorySaver()
    return checkpointer

def get_in_memory_store() -> InMemoryStore:
    """
    Returns an InMemoryStore instance for long-term memory.

    This function creates and returns an InMemoryStore instance that can be used to store and retrieve
    long-term memory in a LangGraph application.

    Returns:
        InMemoryStore: An instance of InMemoryStore for long-term memory.
    """
    store = InMemoryStore()
    return store