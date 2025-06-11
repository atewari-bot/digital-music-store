from agents.music_catalog.edge.music_assistant_tool_edge import should_continue
from agents.music_catalog.nodes.music_assistant_node import music_assistant
from agents.music_catalog.nodes.music_tool_node import get_music_tool_node
from da.memory import get_checkpointer, get_in_memory_store
from da.state import State
from langgraph.graph import StateGraph, START, END
from utils.agent_graph_display import show_graph


def get_music_assistant_agent():
    """
    Orchestrates the music assistant workflow.
    
    This function sets up the music assistant workflow by defining the nodes and edges in the state graph.
    
    Args:
        state (State): The current state of the conversation, including user preferences and message history.
        config (RunnableConfig): Configuration for the runnable, including any necessary parameters.
        
    Returns:
        StateGraph: The compiled state graph for the music catalog subagent.
    """
    music_workflow = StateGraph(State)

    music_workflow.add_node('music_assistant', music_assistant)
    music_workflow.add_node('music_tool_node', get_music_tool_node())

    music_workflow.add_edge(START, 'music_assistant')

    music_workflow.add_conditional_edges(
        'music_assistant', 
        should_continue,
        {
          "continue": "music_tool_node",
          "end": END
        }
    )

    music_workflow.add_edge('music_tool_node', 'music_assistant')

    music_catalog_subagent = music_workflow.compile(name="music_catalog_subagent", checkpointer=get_checkpointer(), store=get_in_memory_store())

    return music_catalog_subagent


def show_music_catalog_subagent_graph():
    """
    Displays the music catalog subagent workflow graph.
    
    This function generates and displays the graph representation of the music catalog subagent workflow.
    """
    show_graph(get_music_assistant_agent(), "Music Catalog Subagent Workflow")