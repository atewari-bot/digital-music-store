from langchain_openai import ChatOpenAI

def get_llm(model_name: str = "meta-llama/Llama-3.3-70B-Instruct") -> ChatOpenAI:
    """
    Returns a ChatOpenAI instance configured with the specified model name.
    
    Args:
        model_name (str): The name of the OpenAI model to use. Default is "meta-llama/Llama-3.3-70B-Instruct".
    
    Returns:
        ChatOpenAI: An instance of ChatOpenAI configured with the specified model.
    """
    return ChatOpenAI(model=model_name, temperature=0.0)