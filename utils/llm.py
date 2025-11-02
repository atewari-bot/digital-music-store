import os
from langchain_openai import ChatOpenAI
from agents.music_catalog.tools import music_tools
import logging

try:
    from langchain_together import ChatTogether
    TOGETHER_AVAILABLE = True
except ImportError:
    TOGETHER_AVAILABLE = False
    logging.warning("langchain-together not available. Install with: pip install langchain-together")

def get_llm(model_name: str = None):
    """
    Returns an LLM instance configured with the specified model name.
    
    Supports both OpenAI and Together AI models based on environment variables.
    
    Args:
        model_name (str): The name of the model to use. If None, will auto-detect based on env vars.
                         For OpenAI: "gpt-4", "gpt-3.5-turbo", etc.
                         For Together: "meta-llama/Llama-3.3-70B-Instruct", etc.
    
    Returns:
        ChatOpenAI or ChatTogether: An instance of the LLM configured with the specified model.
    """
    # Check for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    together_key = os.getenv("TOGETHER_API_KEY")
    
    # Auto-detect model if not provided
    if model_name is None:
        if together_key and TOGETHER_AVAILABLE:
            model_name = "meta-llama/Llama-3.3-70B-Instruct"
        elif openai_key:
            model_name = "gpt-3.5-turbo"
        else:
            raise ValueError(
                "No API key found. Please set either OPENAI_API_KEY or TOGETHER_API_KEY "
                "in your environment variables or .env file."
            )
    
    # Determine if this is a Together AI model
    is_together_model = model_name.startswith("meta-llama") or model_name.startswith("mistralai") or "/" in model_name
    
    # Use Together AI if available and model name suggests it
    if is_together_model and TOGETHER_AVAILABLE and together_key:
        logging.info(f"Using Together AI model: {model_name}")
        return ChatTogether(
            model=model_name,
            temperature=0.0,
            together_api_key=together_key
        )
    
    # Fall back to OpenAI
    if not openai_key:
        if is_together_model:
            raise ValueError(
                "Together AI model specified but TOGETHER_API_KEY not found. "
                "Please set TOGETHER_API_KEY in your environment variables or .env file."
            )
        else:
            raise ValueError(
                "OpenAI model specified but OPENAI_API_KEY not found. "
                "Please set OPENAI_API_KEY in your environment variables or .env file."
            )
    
    logging.info(f"Using OpenAI model: {model_name}")
    return ChatOpenAI(model=model_name, temperature=0.0)

def get_llm_bind(llm):
    """
    Binds the provided LLM to music tools.
    
    This function binds tools to the LLM instance, allowing it to call music-related tools.
    
    Args:
        llm: The LLM instance (ChatOpenAI or ChatTogether) to bind.
    
    Returns:
        The LLM instance with tools bound.
    """
    logging.info("Binding LLM to music tools.")
    return llm.bind_tools(music_tools.get_music_tools())