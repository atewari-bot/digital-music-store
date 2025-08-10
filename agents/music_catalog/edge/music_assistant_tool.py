from da.state import State
from langchain_core.runnables import RunnableConfig

# Define a conditional edge function named `should_continue`
# This function determines next steps based on the state of the conversation
def should_continue(state: State, config: RunnableConfig) -> str:
    """
    Determines whether the music assistant should continue processing based on the state and configuration.
    
    This function checks if the remaining steps in the state are greater than 0, indicating that there are still steps to process.
    
    Args:
        state (State): The current state of the conversation, including user preferences and message history.
        config (RunnableConfig): Configuration for the runnable, including any necessary parameters.
        
    Returns:
        str: "yes" if there are remaining steps, otherwise "no".
    """
    # Get the list of messages from the state
    messages = state["messages"]
    last_message = messages[-1] if messages else None

    # Check if the last message is a ToolMessage and has tool calls
    # LLM generate `tool_calls` when they decide to use a tool
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"