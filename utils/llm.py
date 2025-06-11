from langchain_openai import ChatOpenAI
from agents.music_catalog.tools import music_tools
import logging

def get_llm(model_name: str = "meta-llama/Llama-3.3-70B-Instruct") -> ChatOpenAI:
    """
    Returns a ChatOpenAI instance configured with the specified model name.
    
    Args:
        model_name (str): The name of the OpenAI model to use. Default is "meta-llama/Llama-3.3-70B-Instruct".
    
    Returns:
        ChatOpenAI: An instance of ChatOpenAI configured with the specified model.
    """
    return ChatOpenAI(model=model_name, temperature=0.0)

def get_llm_bind(llm: ChatOpenAI):
    """
    Binds the provided LLM to the global context.
    
    This function sets the global LLM to the provided instance, allowing it to be used throughout the application.
    
    Args:
        llm (ChatOpenAI): The ChatOpenAI instance to bind.
    
    Returns:
        ChatOpenAI: The bound ChatOpenAI instance.
    """
    logging.info("Binding LLM to music tools.")
    return llm.bind_tools(music_tools.get_music_tools())