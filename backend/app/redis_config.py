import os

import redis

def _get_redis():
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', 6379)
    redis_password = os.getenv('REDIS_PASSWORD', None)

    return redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

redis_client = _get_redis()
