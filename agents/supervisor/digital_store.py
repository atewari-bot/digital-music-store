from agents.invoice_info.invoice_info_agent import get_invoice_agent
from agents.music_catalog.music_catalog_agent import get_music_assistant_agent
from da.memory import get_checkpointer, get_in_memory_store
from langgraph_supervisor import create_supervisor
from utils.agent_graph_display import show_graph
import utils.llm as llm_utils
from da.state import State

def get_digital_store_agent_prompt() -> str:
    """
    Returns the prompt for the digital store agent.

    This function provides the prompt that guides the digital store agent in its operations.

    Returns:
        str: The prompt for the digital store agent.
    """
    return (
        """
        You are an expert customer support assistant for a digital music store. 
        You are dedicated to providing exceptional service and ensuring customer queries are answered thoroughly. 
        You have a team of subagents that you can use to help answer queries from customers. 
        Your primary role is to serve as a supervisor/planner for this multi-agent team that helps answer queries from customers. 

        Your team is composed of two subagents that you can use to help answer the customer's request:
        1. music_catalog_information_subagent: this subagent has access to user's saved music preferences. It can also retrieve information about the digital music store's music 
        catalog (albums, tracks, songs, etc.) from the database. 
        3. invoice_information_subagent: this subagent is able to retrieve information about a customer's past purchases or invoices 
        from the database. 

        Based on the existing steps that have been taken in the messages, your role is to generate the next subagent that needs to be called. 
        This could be one step in an inquiry that needs multiple sub-agent calls.
        """
    )


def get_digital_store_agent():
    """
    Digital Store Agent function to handle customer queries in a digital music store.
    This function generates a system message for the digital store agent, which is used to guide the agent's responses
    based on the user's preferences and previous interactions.
    Returns:
        Runnable: A runnable that provides context and instructions for the digital store agent.
    """
    supervisor_agent_workflow = create_supervisor(
        agents=[get_music_assistant_agent(), get_invoice_agent()],
        output_mode="last_message",
        model=llm_utils.get_llm(),
        prompt=get_digital_store_agent_prompt(), 
        state_schema=State
    )

    supervisor_agent = supervisor_agent_workflow.compile(
        name="digital_store_agent",
        checkpointer=get_checkpointer(),
        store=get_in_memory_store()
    )
    return supervisor_agent

def show_digital_store_graph():
    """
    Displays the digital store agent workflow graph.
    
    This function generates and displays the graph representation of the digital store agent workflow.
    """
    show_graph(get_digital_store_agent(), "Digital Store Agent Workflow")