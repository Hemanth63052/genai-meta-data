from scripts.services import login_router
from scripts.schemas.login_schemas import SignupSchema, ChangePasswordSchema, LoginSchema
from scripts.handlers.login_handler import LoginHandler
from fastapi import Response,Request

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
async def login(request_payload: LoginSchema, response: Response, request: Request):
    """
    Login a user.

    This endpoint allows a user to login to their account.

    Args:
        request_payload (SignupSchema): The payload containing the user details.
        response: Fastapi response
        request: Fastapi request

    Returns:
        ResponseModel: A response model indicating the result of the login operation.

    Raises:
        HTTPException: If there is an error logging in the user.
    """
    return LoginHandler().login(request_payload=request_payload, response=response, request=request)

@login_router.post("/logout")
async def logout(user_id, request: Request):
    """
    Logout a user.

    This endpoint allows a user to logout of their account.

    Args:
        user_id (str): The ID of the user to logout.

    Returns:
        ResponseModel: A response model indicating the result of the logout operation.

    Raises:
        HTTPException: If there is an error logging out the user.
    """
    return LoginHandler().logout(user_id=user_id, request=request)

@login_router.post("/forgot-password")
async def forgot_password(request_payload: ChangePasswordSchema):
    """
    Forgot password.

    This endpoint allows a user to reset their password.

    Args:
        request_payload (ChangePasswordSchema): The payload containing the user email.

    Returns:
        ResponseModel: A response model indicating the result of the forgot password operation.

    Raises:
        HTTPException: If there is an error resetting the password.
    """
    return LoginHandler().change_password(request_payload=request_payload)

@login_router.post("/delete-account")
async def delete_account(request_payload: LoginSchema):
    """
    Delete account.

    This endpoint allows a user to delete their account.

    Args:
        request_payload (LoginSchema): The payload containing the user email and password.

    Returns:
        ResponseModel: A response model indicating the result of the delete account operation.

    Raises:
        HTTPException: If there is an error deleting the account.
    """
    return LoginHandler().delete_user(request_payload=request_payload)
