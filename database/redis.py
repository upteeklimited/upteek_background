import redis.asyncio as redis_asyncio
import redis
from settings.config import load_env_config


config = load_env_config()

REDIS_URL = f"redis://:{config['redis_password']}@localhost:6379"

redis_asyncio_client = redis.asyncio.from_url(REDIS_URL, decode_responses=True)
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
