import redis.asyncio as redis
import json
from typing import Optional
from config import REDIS_URL

class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(REDIS_URL, decode_responses=True)

    async def set(self, key: str, value: dict, expire: int = 3600):
        if self.redis:
            await self.redis.set(key, json.dumps(value), ex=expire)

    async def get(self, key: str) -> Optional[dict]:
        if self.redis:
            data = await self.redis.get(key)
            return json.loads(data) if data else None

    async def close(self):
        if self.redis:
            await self.redis.close()


redis_cache = RedisCache()
