import redis
from scripts.config import RedisConfig

def get_redis_client(db):
    return redis.from_url(url=RedisConfig.REDIS_URI, db=db)