from fastapi import HTTPException, status, Request, Response
from scripts.config import JWTConfig
from scripts.logging import logger
from scripts.utils.access_token_decorator import TokenDecorator

class AuthorizationUtil:

    def authorize(self, request: Request, response: Response, token: str = "access_token") -> bool:
        """
        Authorize the Exposed API.
        Args:
            request: The incoming HTTP request.
            response: The outgoing HTTP response.
            token: The token to be validated (default is "access_token").
        Returns:
            bool: True if the API key is valid, False otherwise.
        """

        return True if self.perform_action(request=request, response=response, token=token) else False

    @staticmethod
    def perform_action(request: Request, response: Response, token:str = "access_token")-> str:
        if not request.cookies:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Unauthorized User: API Key is missing")

        try:
            decoded_token, jwt_token = TokenDecorator().validate_token(token=request.cookies.get(token))
            if not decoded_token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail="Unauthorized User: API Key is invalid")

            # Reissue a new token with updated expiration time
            response.set_cookie(key=decoded_token.sub,
                                value=TokenDecorator().create_access_token(mail=jwt_token.mail,
                                                                           host=request.client.host,
                                                                           token_time=JWTConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
                                                                           user_id=decoded_token.user_id),
                                httponly=True)
            return decoded_token.user_id
        except Exception as e:
            logger.exception(f"Error while authorizing the Exposed API: {e}")
            raise e

    def __call__(self, request: Request, response: Response) -> bool:
        """
        Call the Exposed API authentication.
        Args:
            request: The incoming HTTP request.
        Returns:
            bool: True if the API key is valid, False otherwise.
        """
        return self.authorize(request=request, response=response)


class Email(AuthorizationUtil):

    def authorize(self, request: Request, response: Response, token:str ="access_token") -> str:
        """
        Authorize the Exposed API and retrieve the email.
        Args:
            request: The incoming HTTP request.
            response: The outgoing HTTP response.
            token: The token to be validated (default is "access_token").
        Returns:
            str: The email ID of the user if authorized.
        """
        return self.perform_action(request=request, response=response, token=token)
