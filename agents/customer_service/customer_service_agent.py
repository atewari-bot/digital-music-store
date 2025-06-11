import ast
from typing import Optional

from da.db import get_chinook_db

def get_customer_service_agent_prompt() -> str:
    """
    Returns the prompt for the customer service agent.

    This function provides the prompt that guides the customer service agent in its operations.

    Returns:
        str: The prompt for the customer service agent.
    """
    return (
        """You are a customer service representative responsible for extracting customer identifier.\n 
        Only extract the customer's account information from the message history. 
        If they haven't provided the information yet, return an empty string for the file
        and ask them to provide their customer ID, email, or phone number.\n
        You are not allowed to answer any other questions or provide any other information.\n
        You are only allowed to extract the customer identifier from the message history.\n"""
    )

def get_customer_id_from_identifier(identifier: str) -> Optional[int]:
    """
    Extracts the customer ID from the provided identifier.

    Args:
        identifier (str): The identifier which can be a customer ID, email, or phone number.

    Returns:
        Optional[int]: The extracted customer ID or None if not found.
    """
    identifier = identifier.strip()
    if identifier.isdigit():
        return int(identifier)
    elif identifier[0] == '+' and identifier[1:].isdigit():
        query = f"SELECT CustomerId FROM Customer WHERE Phone = '{identifier}'"
        result = get_chinook_db().run(query)
        formatted_result = ast.literal_eval(result)
        if formatted_result:
            return formatted_result[0]['CustomerId']
    elif '@' in identifier:
        query = f"SELECT CustomerId FROM Customer WHERE Email = '{identifier}'"
        result = get_chinook_db().run(query)
        formatted_result = ast.literal_eval(result)
        if formatted_result:
            return formatted_result[0]['CustomerId']
    return None