from da.state import State
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
import utils.llm as llm_utils
from da.memory_utils import save_user_preferences, extract_preferences_from_messages
import logging


def generate_music_assistant_prompt(memory: str = "None") -> str:
    """
    Generates a prompt for the music assistant.
    
    This function creates a system message that instructs the assistant to help users find music-related information
    such as albums, artists, and genres. It also provides examples of how to use the assistant.
    
    Returns:
        str: The generated system message prompt.
    """
    return f"""
    You are a member of the assistant team, your role specifically is to focused on helping customers discover and learn about music in our digital catalog. 
    If you are unable to find playlists, songs, or albums associated with an artist, it is okay. 
    Just inform the customer that the catalog does not have any playlists, songs, or albums associated with that artist.
    You also have context on any saved user preferences, helping you to tailor your response. 
    
    CORE RESPONSIBILITIES:
    - Search and provide accurate information about songs, albums, artists, and playlists
    - Offer relevant recommendations based on customer interests
    - Handle music-related queries with attention to detail
    - Help customers discover new music they might enjoy
    - You are routed only when there are questions related to music catalog; ignore other questions. 
    
    SEARCH GUIDELINES:
    1. Always perform thorough searches before concluding something is unavailable
    2. If exact matches aren't found, try:
       - Checking for alternative spellings
       - Looking for similar artist names
       - Searching by partial matches
       - Checking different versions/remixes
    3. When providing song lists:
       - Include the artist name with each song
       - Mention the album when relevant
       - Note if it's part of any playlists
       - Indicate if there are multiple versions
    
    Additional context is provided below: 

    Prior saved user preferences: {memory}
    
    Message history is also attached.  
    """

def music_assistant(state: State, config: RunnableConfig):
    """
    Music Assistant function to handle music-related queries.
    
    This function generates a system message for the music assistant, which is used to guide the assistant's responses
    based on the user's preferences and previous interactions.
    
    Args:
        state (State): The current state of the conversation, including user preferences and message history.
        config (RunnableConfig): Configuration for the runnable, including any necessary parameters.
        
    Returns:
        SystemMessage: A system message that provides context and instructions for the music assistant.
    """
    memory = state.get('loaded_memory', "None")
    customer_id = state.get('customer_id', "")

    # Extract and save preferences if detected in messages
    if customer_id and customer_id != "":
        extracted_prefs = extract_preferences_from_messages(state.get('messages', []))
        if extracted_prefs and extracted_prefs != "None":
            save_user_preferences(customer_id, extracted_prefs, config)
            # Update memory if new preferences were found
            if memory == "None" or memory == "":
                memory = extracted_prefs

    music_assistant_prompt = generate_music_assistant_prompt(memory)
    llm_with_music_tools = llm_utils.get_llm_bind(llm_utils.get_llm())

    response = llm_with_music_tools.invoke(
        [SystemMessage(content=music_assistant_prompt)] + state.get('messages', []))
    
    logging.debug("Response from LLM: %s", response)

    return {'messages': [response]}

 