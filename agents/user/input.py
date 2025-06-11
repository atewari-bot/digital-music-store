import logging
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from da.state import State, UserInput
from langgraph.types import interrupt


def get_user_input(state: State, config: RunnableConfig)  -> dict:
    """
    Prompts the user for input and returns the response.

    This function is used to gather user input, which can be a customer ID, email, or phone number.
    
    Returns:
        dict: A dictionary containing the user input message.
    """
    user_input = interrupt("Please enter your customer ID, email, or phone number:")
    if not user_input:
        raise ValueError("User input cannot be empty.")

    logging.error(f"User input received: {user_input}")
    
    return {"messages": [user_input]}

def get_user_input_bind(llm: ChatOpenAI):
    """
    Binds the user input schema to the LLM.
    This function configures the LLM to use a structured output schema for user input.
    Args:
        llm (ChatOpenAI): The ChatOpenAI instance to bind.
    """
    logging.info("Binding user input schema to LLM.")
    try:
        return llm.with_structured_output(
            schema=UserInput,
            description="User input for customer ID, email, or phone number.",
        )
    except Exception as e:
        logging.error(f"Error binding user input schema: {e}")
      
