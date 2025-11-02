from agents.supervisor.digital_store import get_digital_store_agent
from langchain_core.messages import HumanMessage
from utils.state_utils import create_initial_state
import uuid
import logging

def test_digital_store_agent():
    """
    Test the digital store agent's orchestration.
    
    This function tests the digital store agent by invoking it with a sample question and checking the response.
    """
    thread_id = str(uuid.uuid4())
    question = "My customer ID is 1. How much was my most recent purchase? What albums do you have by U2?"
    config = {"configurable": {"thread_id": thread_id}}

    logging.debug(f"Testing digital store agent with thread_id: {thread_id} and question: {question}")

    try:
        # Create initial state with proper initialization
        state = create_initial_state(question, config=config)
        
        # Invoke the digital store orchestration with the question
        result = get_digital_store_agent().invoke(state, config=config)

        print("\n" + "="*60)
        print("Test Results:")
        print("="*60)
        for message in result['messages']:
            if hasattr(message, 'pretty_print'):
                message.pretty_print()
            elif hasattr(message, 'content'):
                print(f"\n{message.content}")
        
        print("\n" + "="*60)
        return result
    except Exception as e:
        logging.error(f"Error in test: {e}", exc_info=True)
        raise