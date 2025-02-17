from scripts.services import login_router
from scripts.schemas.login_schemas import SignupSchema
from scripts.handlers.login_handler import LoginHandler
from fastapi import Response

@login_router.post("/signup")
async def signup(request_payload: SignupSchema):
    """
    Signup a new user.

    This endpoint allows a user to signup a new account.

    Args:
        request_payload (SignupSchema): The payload containing the user details.

    Returns:
        ResponseModel: A response model indicating the result of the signup operation.

    Raises:
        HTTPException: If there is an error signing up the user.
    """
    return LoginHandler().signup(request_payload)

@login_router.post("/login")
async def login(request_payload: SignupSchema, response: Response):
    """
    Login a user.

    This endpoint allows a user to login to their account.

    Args:
        request_payload (SignupSchema): The payload containing the user details.

    Returns:
        ResponseModel: A response model indicating the result of the login operation.

    Raises:
        HTTPException: If there is an error logging in the user.
    """
    return LoginHandler().login(request_payload=request_payload, response=response)

