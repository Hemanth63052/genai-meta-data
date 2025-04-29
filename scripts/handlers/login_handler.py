from adapt_iq_common.config import JWTConfig
from adapt_iq_common.exceptions import GenAIException
from scripts.schemas import ReturnSuccessSchema
from scripts.schemas.login_schemas import SignupSchema, LoginSchema, ChangePasswordSchema
from adapt_iq_common.utils.access_token_decorator import TokenDecorator
from adapt_iq_common.utils.mongo_util.user import User
from adapt_iq_common.utils.hash_util import HashUtil
from fastapi import Response, Request, status

class LoginHandler:

    def __init__(self) -> None:
        self.user_collection = User()
        self.hash_util = HashUtil()

    def signup(self, request_payload: SignupSchema):
        """
        Register a new user.

        This endpoint allows a user to register a new account.

        Args:
            request_payload (SignupSchema): The payload containing the user's email and password.

        Returns:
            ResponseModel: A response model indicating the result of the signup operation.

        Raises:
            HTTPException: If there is an error registering the user.
        """
        if not request_payload.email or not request_payload.password:
            raise GenAIException("Email and password are required.", code=status.HTTP_400_BAD_REQUEST)
        if self.user_collection.find_one({"email": request_payload.email}):
            raise GenAIException("User already exists. Please login.", code=status.HTTP_400_BAD_REQUEST)
        request_payload.password = self.hash_util.hash_password(request_payload.password)
        self.user_collection.insert_one(request_payload.model_dump())
        return ReturnSuccessSchema(message="User registered successfully. Please Login")

    def login(self, request_payload: LoginSchema, response: Response, request: Request):
        """
        Log in a user.

        This endpoint allows a user to log in to their account.

        Args:
            request_payload (LoginSchema): The payload containing the user's email and password.
            response: Fastapi response
            request: Fastapi request

        Returns:
            ResponseModel: A response model indicating the result of the login operation.

        Raises:
            HTTPException: If there is an error logging in the user.
        """
        if not request_payload.email or not request_payload.password:
            raise GenAIException("Email and password are required.", code=status.HTTP_400_BAD_REQUEST)
        user = self.user_collection.find_one({"email": request_payload.email})
        if not user:
            raise GenAIException("User not found.", code=status.HTTP_404_NOT_FOUND)
        if not self.hash_util.compare_password(request_payload.password, user["password"]):
            raise GenAIException("Invalid password.", code=status.HTTP_401_UNAUTHORIZED)
        response.set_cookie(key="access_token", value=TokenDecorator().create_access_token(mail=request_payload.email, host=request.client.host, token_time=JWTConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES, user_id=user["user_id"]),
                            httponly=True)
        response.set_cookie(key="refresh_token", value=TokenDecorator().create_access_token(mail=request_payload.email, host=request.client.host, sub="refresh_token", token_time=JWTConfig.JWT_REFRESH_TOKEN_EXPIRE_MINUTES, user_id=user["user_id"]),
                            httponly=True)
        return ReturnSuccessSchema(message="User logged in successfully.")

    def logout(self, user_id, request: Request):
        """
        Log out a user.

        This endpoint allows a user to log out of their account.

        Args:
            user_id (str): The ID of the user to log out.
            request: Fastapi request

        Returns:
            ResponseModel: A response model indicating the result of the logout operation.

        Raises:
            HTTPException: If there is an error logging out the user.
        """
        user = self.user_collection.find({"user_id": user_id})
        if not user:
            raise GenAIException("User not found.", code=status.HTTP_404_NOT_FOUND)
        TokenDecorator().delete_access_token_from_db(request.cookies)
        return ReturnSuccessSchema(message="User logged out successfully.")

    def change_password(self, request_payload:ChangePasswordSchema):
        """
        Change a user's password.

        This endpoint allows a user to change their account password.

        Args:
            request_payload (ChangePasswordSchema): The payload containing the user's email and new password.

        Returns:
            ResponseModel: A response model indicating the result of the password change operation.

        Raises:
            HTTPException: If there is an error changing the user's password.
        """
        if not request_payload.new_password:
            raise GenAIException("New password is required.", code=status.HTTP_400_BAD_REQUEST)
        if not request_payload.email or not request_payload.new_password:
            raise GenAIException("Email and old password are required.", code=status.HTTP_400_BAD_REQUEST)
        user = self.user_collection.find_one({"email": request_payload.email})
        if not user:
            raise GenAIException("User not found.", code=status.HTTP_404_NOT_FOUND)
        if not self.hash_util.compare_password(request_payload.password, user["password"]):
            raise GenAIException("Invalid Old password.", code=status.HTTP_401_UNAUTHORIZED)
        self.user_collection.update_one({"email": request_payload.email, "password": user["password"]}, {"$set": {"password": self.hash_util.hash_password(request_payload.new_password)}})
        return ReturnSuccessSchema(message="Password changed successfully.")

    def delete_user(self, request_payload: LoginSchema):
        """
        Delete a user.

        This endpoint allows a user to delete their account.

        Args:
            request_payload (LoginSchema): The payload containing the user's email and password.

        Returns:
            ResponseModel: A response model indicating the result of the user deletion operation.

        Raises:
            HTTPException: If there is an error deleting the user.
        """
        if not request_payload.email or not request_payload.password:
            raise GenAIException("Email and password are required.")
        user = self.user_collection.find_one({"email": request_payload.email})
        if not user:
            raise GenAIException("User not found.", code=status.HTTP_404_NOT_FOUND)
        if not self.hash_util.compare_password(request_payload.password, user["password"]):
            raise GenAIException("Invalid password.", code= status.HTTP_401_UNAUTHORIZED)
        self.user_collection.delete_one({"email": request_payload.email})
        return ReturnSuccessSchema(message="User deleted successfully.")
