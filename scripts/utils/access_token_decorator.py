import datetime
import json

from fastapi import status
from pydantic import BaseModel

from scripts.utils.jwt_util import JWTUtil
from scripts.utils.redis_util import get_redis_client
from scripts.exception import GenAIException

class JWTSchema(BaseModel):
    mail: str
    host: str
    sub: str
    iat: int = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

class TokenSchema(BaseModel):
    user_id: str
    sub: str
    host: str
    iat: int = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


class TokenDecorator:
    def __init__(self):
        self.redis_login_client = get_redis_client(db=0)
        self.jwt_util = JWTUtil()

    def create_access_token(self, mail, host,user_id, sub="access_token", token_time=60 * 10):
        jwt_dict = JWTSchema(mail=mail, host=host, sub=sub).model_dump()
        jwt_token = self.jwt_util.encode(jwt_dict)
        self.redis_login_client.set(jwt_token, TokenSchema(user_id=user_id, host=host, sub=sub).model_dump_json(), token_time)
        return jwt_token

    def validate_token(self, token) -> (TokenSchema, JWTSchema):
        redis_data = self.redis_login_client.get(token)
        if not redis_data:
            raise GenAIException("Token is invalid or expired", status.HTTP_401_UNAUTHORIZED)
        return TokenSchema(**json.loads(redis_data)), JWTSchema(** self.jwt_util.decode(token))

    def delete_access_token_from_db(self, token):
        self.redis_login_client.delete(token)
        return True
