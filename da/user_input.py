from pydantic import BaseModel, Field

class UserInput(BaseModel):
    """
    Represents user input for a task.
    """
    identifier: str = Field(description="Identifier which can be - Customer ID, email, or phone number")
  