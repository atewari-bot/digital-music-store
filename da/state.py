from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps

class State(TypedDict, total=False):
    """
    Represents the state of a LangGraph agent.

    This state is used to manage the flow of messages and steps in a LangGraph agent.
    It includes the customer_id, remaining steps, long term memory and any additional data needed for processing.
    """
    # customer_id: The ID of the customer being processed
    customer_id: str

    # messages: List of messages in the conversation history
    # Annotated with `add_messages` to allow appending of messages to the conversation
    messages: Annotated[list[AnyMessage], add_messages]

    # remaining_steps: Used by LangGraph to determine how many steps are left in the process to prevent infinite loops
    remaining_steps: RemainingSteps

    # loaded_memory: Stores information loaded from long-term memory like user preferences, historical context
    loaded_memory: str
    
    # next_agent: Used by supervisor to route to the next agent
    next_agent: str