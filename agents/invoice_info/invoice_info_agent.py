from agents.invoice_info.tools.invoice_tools import get_invoice_tools
from da.state import State
from da.memory import get_checkpointer, get_in_memory_store
from langgraph.prebuilt import create_react_agent
from utils.agent_graph_display import show_graph
import utils.llm as llm_utils
import logging

def get_invoice_agent_prompt() -> str:
    """
    Returns the prompt for the invoice information agent.
    
    This function provides the prompt that guides the invoice information agent in its operations.
    
    Returns:
        str: The prompt for the invoice information agent.
    """
    return (
      """
      You are a subagent among a team of assistants. You are specialized for retrieving and processing invoice information. You are routed for invoice-related portion of the questions, so only respond to them.

      You have access to three tools. These tools enable you to retrieve and process invoice information from the database. Here are the tools:
      - get_invoices_by_customer_sorted_by_date: This tool retrieves all invoices for a customer, sorted by invoice date.
      - get_invoices_sorted_by_unit_price: This tool retrieves all invoices for a customer, sorted by unit price.
      - get_employee_by_invoice_and_customer: This tool retrieves the employee information associated with an invoice and a customer.
      
      If you are unable to retrieve the invoice information, inform the customer you are unable to retrieve the information, and ask if they would like to search for something else.
      
      CORE RESPONSIBILITIES:
      - Retrieve and process invoice information from the database
      - Provide detailed information about invoices, including customer details, invoice dates, total amounts, employees associated with the invoice, etc. when the customer asks for it.
      - Always maintain a professional, friendly, and patient demeanor
      
      You may have additional context that you should use to help answer the customer's query. It will be provided to you below:
      """
    )

def get_invoice_agent():
    """
    Invoice Agent function to handle invoice-related queries.
    
    This function generates a system message for the invoice agent, which is used to guide the agent's responses
    based on the user's preferences and previous interactions.
    
    Args:
        state (State): The current state of the conversation, including user preferences and message history.
        
    Returns:
        Runnable: A runnable that provides context and instructions for the invoice agent.
    """
    invoice_information_subagent = create_react_agent(
        llm_utils.get_llm(),
        tools=get_invoice_tools(),
        prompt=get_invoice_agent_prompt(),
        name="invoice_info_agent",
        state_schema=State,
        checkpointer=get_checkpointer(),
        store=get_in_memory_store()
    )
    logging.info("Created invoice info agent with tools: %s", get_invoice_tools())
    return invoice_information_subagent

def show_invoice_info_subagent_graph():
    """
    Displays the invoice information subagent workflow graph.
    
    This function generates and displays the graph representation of the invoice information subagent workflow.
    """
    show_graph(get_invoice_agent(), "Invoice Information Subagent Workflow")

