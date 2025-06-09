import uuid
import sys
import os
from agents.music_catalog.music_catalog_agent import get_music_assistant_orchestration
from langchain_core.messages import HumanMessage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_music_catalog_agent():
    """
    Test the music catalog agent's orchestration.
    
    This function tests the music catalog agent by invoking it with a sample question and checking the response.
    """
    thread_id = uuid.uuid4()
    question = "I like the Rolling Stones. What songs do you recommend by them or by other artists that I might like?"
    config = {"configurable": {"thread_id": thread_id}}

    result = get_music_assistant_orchestration().invoke({"messages": [HumanMessage(content=question)]}, config=config)
    print(result)
    for message in result['messages']:
      message.pretty_print()

def __main__():
    """
    Main function to run the test.
    
    This function is the entry point for running the music catalog agent test.
    """
    test_music_catalog_agent()