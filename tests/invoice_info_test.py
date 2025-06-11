import logging
import uuid
from agents.invoice_info.invoice_info_agent import get_invoice_agent
from langchain_core.messages import HumanMessage

def test_invoice_info_agent():
    """
    Test the invoice info agent's orchestration.
    
    This function tests the invoice info agent by invoking it with a sample question and checking the response.
    """
    thread_id = uuid.uuid4()
    question = "My customer id is 1. What is the total amount due on my latest invoice?"
    # question = "My customer id is 1. What was my most recent invoice, and who was the employee that helped me with it?"
    config = {"configurable": {"thread_id": thread_id}}
    
    logging.debug(f"Testing invoice info agent with thread_id: {thread_id} and question: {question}")
    
    # Invoke the invoice info orchestration with the question
    result = get_invoice_agent().invoke({"messages": [HumanMessage(content=question)]}, config=config)
    
    for message in result['messages']:
        message.pretty_print()