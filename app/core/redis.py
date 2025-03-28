import redis.asyncio as redis
import json
from typing import Optional, Any
from config import settings

class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(settings.REDIS_HOST + settings.REDIS_PORT, decode_responses=True)

    async def set(self, key: str, value: Any, expire: int = 3600):
        if self.redis:
            # value может быть списком, словарём и т.д.
            await self.redis.set(key, json.dumps(value), ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        if self.redis:
            data = await self.redis.get(key)
            return json.loads(data) if data else None

    async def close(self):
        if self.redis:
            await self.redis.close()

redis_cache = RedisCache()
