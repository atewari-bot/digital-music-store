from langgraph.prebuilt import ToolNode
from agents.music_catalog.tools import music_tools

def get_music_tool() -> ToolNode:
    """
    Returns a ToolNode instance for music-related operations.
    
    This function creates and returns a ToolNode instance that can be used to interact with music-related functionalities.
    
    Returns:
        ToolNode: An instance of ToolNode configured for music operations.
    """
    tool_node = ToolNode(music_tools.get_muscic_tools())

    return tool_node