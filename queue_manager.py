import json
from typing import AsyncGenerator

import redis.asyncio as redis

from log_config import get_logger
from settings import settings

logger = get_logger(__name__)


class QueueManager:
    def __init__(self, task_id: str, redis_url: str = f'redis://{settings.REDIS_HOST}:6379'):
        self.redis_url = redis_url
        self._redis_client = None
        self.task_id = task_id

    async def get_redis(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = await redis.from_url(self.redis_url)
        return self._redis_client

    async def publish(self, data: dict):
        redis_client = await self.get_redis()
        key = f"translation:{self.task_id}"
        await redis_client.rpush(key, json.dumps(data))

    async def mark_complete(self, expire_seconds: int = 3600):
        redis_client = await self.get_redis()
        key = f"translation:{self.task_id}"
        await redis_client.rpush(key, json.dumps({"status": "complete"}))
        await redis_client.expire(key, expire_seconds)

    async def listen(self, timeout: int = 30) -> AsyncGenerator[dict, None]:
        redis_client = await self.get_redis()
        key = f"translation:{self.task_id}"

        while True:
            try:
                result = await redis_client.blpop(key, timeout=timeout)
                if not result:
                    break

                data = json.loads(result[1])
                logger.info(f"listen: {data}")

                # Check for special exit character
                if data.get("status") == "complete" or data.get("status") == "exit":
                    break

                yield data

            except Exception as e:
                logger.error(f"Error in listen: {e}")
                break
