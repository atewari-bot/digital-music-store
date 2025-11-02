"""
Supervisor utilities for creating multi-agent systems with LangGraph.

This module provides utilities to create a supervisor pattern that routes
queries to different sub-agents based on the query content.
"""
from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from da.state import State
import utils.llm as llm_utils
import logging


def create_supervisor(
    agents: List[Any],
    model=None,
    prompt: str = "",
    state_schema: type = State,
    output_mode: str = "last_message"
):
    """
    Create a supervisor agent that routes queries to sub-agents.
    
    Args:
        agents: List of agent runnables (sub-agents)
        model: LLM model to use for routing decisions
        prompt: System prompt for the supervisor
        state_schema: State schema type
        output_mode: How to output results ("last_message" or "all_messages")
        
    Returns:
        StateGraph: The compiled supervisor graph
    """
    if model is None:
        model = llm_utils.get_llm()
    
    # Create meaningful agent names
    agent_names = ["music_catalog_subagent", "invoice_info_subagent"]
    
    # Ensure we have the right number of agent names
    if len(agent_names) != len(agents):
        agent_names = [f"agent_{i}" for i in range(len(agents))]
    
    # Create a mapping of agent names to agents
    agent_map = {name: agent for name, agent in zip(agent_names, agents)}
    
    def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Supervisor node that decides which agent to call.
        """
        messages = state.get('messages', [])
        if not messages:
            return {}
        
        # Get the last user message
        last_message = messages[-1] if messages else None
        if not last_message or not hasattr(last_message, 'content'):
            return {'next_agent': agent_names[0]}
        
        message_content = last_message.content.lower()
        
        # Simple keyword-based routing (can be enhanced with LLM)
        # Check for invoice-related keywords
        invoice_keywords = ['invoice', 'purchase', 'bill', 'payment', 'order', 'transaction', 'paid']
        if any(keyword in message_content for keyword in invoice_keywords):
            logging.info("Supervisor routing to invoice_info_subagent")
            return {'next_agent': agent_names[1]}
        
        # Check for music-related keywords
        music_keywords = ['album', 'song', 'artist', 'track', 'music', 'genre', 'playlist']
        if any(keyword in message_content for keyword in music_keywords):
            logging.info("Supervisor routing to music_catalog_subagent")
            return {'next_agent': agent_names[0]}
        
        # If both keywords are present or unclear, use LLM to decide
        try:
            routing_prompt = f"""{prompt}

Available agents:
1. {agent_names[0]} - Handles music catalog queries (artists, albums, songs, genres)
2. {agent_names[1]} - Handles invoice and purchase history queries

User message: {last_message.content}

Which agent should handle this query? Respond with ONLY "1" or "2"."""
            
            response = model.invoke([
                SystemMessage(content=routing_prompt),
                HumanMessage(content="Respond with just the number: 1 or 2")
            ])
            
            response_text = response.content.strip() if hasattr(response, 'content') else str(response)
            
            # Extract number from response
            if '1' in response_text:
                selected_agent = agent_names[0]
            elif '2' in response_text:
                selected_agent = agent_names[1]
            else:
                selected_agent = agent_names[0]  # Default to music agent
            
            logging.info(f"Supervisor (LLM) routing to: {selected_agent}")
            return {'next_agent': selected_agent}
            
        except Exception as e:
            logging.error(f"Error in supervisor routing: {e}")
            return {'next_agent': agent_names[0]}  # Default to first agent
    
    def route_to_agent(state: Dict[str, Any]) -> str:
        """
        Routing function that returns the next agent to call.
        """
        next_agent = state.get('next_agent', agent_names[0])
        return next_agent
    
    # Create the supervisor workflow
    workflow = StateGraph(state_schema)
    
    # Add supervisor node
    workflow.add_node("supervisor", supervisor_node)
    
    # Add sub-agent nodes
    for name, agent in agent_map.items():
        workflow.add_node(name, agent)
    
    # Add START edge to supervisor
    workflow.add_edge(START, "supervisor")
    
    # Add conditional edge from supervisor to agents
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {name: name for name in agent_names}
    )
    
    # All agents end after processing
    for name in agent_names:
        workflow.add_edge(name, END)
    
    return workflow


def create_simple_supervisor(
    agents: List[Any],
    agent_names: List[str],
    model=None,
    prompt: str = "",
    state_schema: type = State
):
    """
    Create a simpler supervisor that uses a fixed routing strategy.
    
    Args:
        agents: List of agent runnables
        agent_names: List of agent names (must match order of agents)
        model: LLM model for routing
        prompt: System prompt
        state_schema: State schema type
        
    Returns:
        StateGraph: The compiled supervisor graph
    """
    if len(agents) != len(agent_names):
        raise ValueError("Number of agents must match number of agent names")
    
    if model is None:
        model = llm_utils.get_llm()
    
    agent_map = {name: agent for name, agent in zip(agent_names, agents)}
    
    def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Supervisor node that routes to appropriate agent."""
        messages = state.get('messages', [])
        if not messages:
            return {'messages': [AIMessage(content="No messages to process.")]}
        
        last_message = messages[-1] if messages else None
        if not last_message:
            return {'next_agent': agent_names[0]}
        
        message_content = last_message.content.lower() if hasattr(last_message, 'content') else str(last_message).lower()
        
        # Simple keyword-based routing
        if any(keyword in message_content for keyword in ['invoice', 'purchase', 'bill', 'payment', 'order']):
            if len(agent_names) > 1:  # invoice agent
                return {'next_agent': agent_names[1]}
        
        # Default to music catalog agent
        return {'next_agent': agent_names[0]}
    
    def route_to_agent(state: Dict[str, Any]) -> str:
        """Route to the selected agent."""
        return state.get('next_agent', agent_names[0])
    
    # Build the graph
    workflow = StateGraph(state_schema)
    workflow.add_node("supervisor", supervisor_node)
    
    for name, agent in agent_map.items():
        workflow.add_node(name, agent)
    
    workflow.add_edge(START, "supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {name: name for name in agent_names}
    )
    
    # Add edges back to supervisor for continuation
    for name in agent_names:
        workflow.add_edge(name, END)  # End after each agent response
    
    return workflow

