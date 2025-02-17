from pydantic import BaseModel

class ReturnSuccessSchema(BaseModel):
    """
    Schema for returning a success message.

    Attributes:
        message (str): The success message.
    """

    message: str
    status="success"
    data:dict = {}