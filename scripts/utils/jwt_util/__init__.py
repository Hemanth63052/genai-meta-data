import jwt
from scripts.logging import logger
from scripts.config import JWTConfig


class JWTUtil:

    @staticmethod
    def encode(payload):
        try:
            return jwt.encode(payload, JWTConfig.PRIVATE_KEY, algorithm=JWTConfig.JWT_ALGORITHM)
        except Exception as e:
            logger.error(f"Error encoding JWT: {e}")
            return None

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, JWTConfig.PUBLIC_KEY, algorithms=[JWTConfig.JWT_ALGORITHM])
        except Exception as e:
            logger.error(f"Error decoding JWT: {e}")
            return None
