"""
Main entry point for the Digital Music Store AI Agent.

This script demonstrates how to use the multi-agent system to handle
customer queries about music catalog and invoice information.
"""
import sys
import os
import uuid
import logging
from langchain_core.messages import HumanMessage
from agents.supervisor.digital_store import get_digital_store_agent
from utils.state_utils import create_initial_state
from utils.env import load_environment_variables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def run_example_queries():
    """
    Run example queries to demonstrate the agent's capabilities.
    """
    print("\n" + "="*60)
    print("Digital Music Store AI Agent - Example Queries")
    print("="*60 + "\n")
    
    # Load environment variables
    load_environment_variables()
    
    # Initialize the agent
    agent = get_digital_store_agent()
    
    # Example 1: Music catalog query
    print("\n[Example 1: Music Catalog Query]")
    print("-" * 60)
    thread_id_1 = uuid.uuid4()
    config_1 = {"configurable": {"thread_id": str(thread_id_1)}}
    question_1 = "My customer ID is 1. What albums do you have by U2?"
    
    print(f"Question: {question_1}\n")
    print("Agent Response:")
    try:
        state_1 = create_initial_state(question_1, config=config_1)
        result_1 = agent.invoke(state_1, config_1)
        for message in result_1['messages'][-3:]:  # Show last 3 messages
            if hasattr(message, 'content'):
                print(f"  {message.content[:200]}...")
    except Exception as e:
        logging.error(f"Error in Example 1: {e}")
    
    # Example 2: Invoice query
    print("\n\n[Example 2: Invoice Information Query]")
    print("-" * 60)
    thread_id_2 = uuid.uuid4()
    config_2 = {"configurable": {"thread_id": str(thread_id_2)}}
    question_2 = "My customer ID is 1. How much was my most recent purchase?"
    
    print(f"Question: {question_2}\n")
    print("Agent Response:")
    try:
        state_2 = create_initial_state(question_2, config=config_2)
        result_2 = agent.invoke(state_2, config_2)
        for message in result_2['messages'][-3:]:  # Show last 3 messages
            if hasattr(message, 'content'):
                print(f"  {message.content[:200]}...")
    except Exception as e:
        logging.error(f"Error in Example 2: {e}")
    
    # Example 3: Combined query
    print("\n\n[Example 3: Combined Query]")
    print("-" * 60)
    thread_id_3 = uuid.uuid4()
    config_3 = {"configurable": {"thread_id": str(thread_id_3)}}
    question_3 = "My customer ID is 1. How much was my most recent purchase? Also, what albums do you have by The Rolling Stones?"
    
    print(f"Question: {question_3}\n")
    print("Agent Response:")
    try:
        state_3 = create_initial_state(question_3, config=config_3)
        result_3 = agent.invoke(state_3, config_3)
        for message in result_3['messages'][-3:]:  # Show last 3 messages
            if hasattr(message, 'content'):
                print(f"  {message.content[:200]}...")
    except Exception as e:
        logging.error(f"Error in Example 3: {e}")
    
    # Example 4: Music preference query (will save preferences)
    print("\n\n[Example 4: Music Preference Query]")
    print("-" * 60)
    thread_id_4 = uuid.uuid4()
    config_4 = {"configurable": {"thread_id": str(thread_id_4)}}
    question_4 = "My customer ID is 1. I like the Rolling Stones. What songs do you recommend by them or by other artists that I might like?"
    
    print(f"Question: {question_4}\n")
    print("Agent Response:")
    try:
        state_4 = create_initial_state(question_4, config=config_4)
        result_4 = agent.invoke(state_4, config_4)
        for message in result_4['messages'][-3:]:  # Show last 3 messages
            if hasattr(message, 'content'):
                print(f"  {message.content[:200]}...")
        print("\n  Note: User preferences have been saved for future conversations.")
    except Exception as e:
        logging.error(f"Error in Example 4: {e}")
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")


def interactive_mode():
    """
    Run the agent in interactive mode where users can enter queries.
    """
    print("\n" + "="*60)
    print("Digital Music Store AI Agent - Interactive Mode")
    print("="*60)
    print("Enter your queries below. Type 'exit' or 'quit' to exit.\n")
    
    load_environment_variables()
    agent = get_digital_store_agent()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAgent: ", end="")
            state = create_initial_state(user_input, config=config)
            result = agent.invoke(state, config)
            
            # Get the last message from the agent
            last_message = result['messages'][-1]
            if hasattr(last_message, 'content'):
                print(last_message.content)
            else:
                print("Response received but content not available.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            print(f"Sorry, an error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        run_example_queries()

