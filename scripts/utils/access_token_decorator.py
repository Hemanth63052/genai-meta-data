import time
from scripts.utils.jwt_util import JWTUtil
from scripts.utils.redis_util import get_redis_client
from scripts.exception import GenAIException


class TokenDecorator:
    def __init__(self):
        self.redis_login_client = get_redis_client(db=0)
        self.jwt_util = JWTUtil()

    def create_access_token(self, mail, host, sub="access_token", ):
        jwt_dict = {
            "mail": mail,
            "host": host,
            "sub": sub,
            "iat": time.time()
        }
        jwt_token = self.jwt_util.encode(jwt_dict)
        self.redis_login_client.setx(jwt_token, jwt_dict, 60*10)
        return jwt_token

    def validate_token(self, token):
        redis_data = self.redis_login_client.getx(token)
        if not redis_data:
            return GenAIException("Token is invalid or expired", 401)
        return self.jwt_util.decode(token)

    def delete_access_token_from_db(self, token):
        self.redis_login_client.delete(token)
        return True


