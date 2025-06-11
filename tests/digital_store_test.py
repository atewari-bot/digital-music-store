from agents.supervisor.digital_store import get_digital_store_agent
from langchain_core.messages import HumanMessage
import uuid
import logging

def test_digital_store_agent():
    """
    Test the digital store agent's orchestration.
    
    This function tests the digital store agent by invoking it with a sample question and checking the response.
    """
    thread_id = uuid.uuid4()
    question = "My customer ID is 1. How much was my most recent purchase? What albums do you have by U2?"
    config = {"configurable": {"thread_id": thread_id}}

    logging.debug(f"Testing digital store agent with thread_id: {thread_id} and question: {question}")

    # Invoke the digital store orchestration with the question
    result = get_digital_store_agent().invoke({"messages": [HumanMessage(content=question)]}, config=config)

    for message in result['messages']:
        message.pretty_print()