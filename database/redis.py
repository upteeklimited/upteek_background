import redis.asyncio as redis
from settings.config import load_env_config


config = load_env_config()

redis_client = redis.from_url(f"redis://:{config['redis_password']}@localhost:6379", decode_responses=True)

