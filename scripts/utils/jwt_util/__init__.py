import jwt
from scripts.logging import logger
from scripts.config import JWTConfig

class JWTUtil:
    def __init__(self, public_key_path=JWTConfig.PUBLIC_KEY_PATH, private_key_path=JWTConfig.PRIVATE_KEY_PATH):
        self.public_key_path = public_key_path or "data/public-key"
        self.private_key_path = private_key_path or "data/private-key"

    def encode(self, payload):
        try:
            with open(self.private_key_path, "rb") as private_key:
                private_key = private_key.read()
                return jwt.encode(payload, private_key, algorithm="RS256")
        except Exception as e:
            logger.error(f"Error encoding JWT: {e}")
            return None

    def decode(self, token):
        try:
            with open(self.public_key_path, "rb") as public_key:
                public_key = public_key.read()
                return jwt.decode(token, public_key, algorithms=["RS256"])
        except Exception as e:
            logger.error(f"Error decoding JWT: {e}")
            return None
