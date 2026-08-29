import time
import asyncio
from pydantic import BaseModel
from collections import defaultdict
import detection
from redis.asyncio import Redis
import logging

class Log(BaseModel):
    timestampMs: int
    accountId: str
    ip: str
    operation: str
    method: str
    status: str
    message: str
    userAgent: str

async def anomaliesDetectorLoop(redis_client: Redis) -> None:
    while True:
        now = int(time.time())
        counterJson = defaultdict(lambda: [0, 0, 0])
        for timestamp in range(now - 10, now + 1):
            cursor = 0
            while True:
                cursor, keys = await redis_client.scan(cursor, match=f"rate:{timestamp}:*", count=1000)
                if keys:
                    async with redis_client.pipeline(transaction=False) as pipe:
                        for key in keys:
                            pipe.hgetall(key)
                        results = await pipe.execute()

                        for key, counts in zip(keys, results):
                            ip = key.split(":", 2)[2]
                            counterJson[ip][0] += int(counts.get("all", 0))
                            counterJson[ip][1] += int(counts.get("401", 0))
                            counterJson[ip][2] += int(counts.get("404", 0))
                if cursor == 0:
                    break
        detection.runAllFunctions(counterJson)
        await asyncio.sleep(0.9)

async def processLogs(reqBody: list[Log], redis_client: Redis) -> None:
    counterJson = defaultdict(int)
    async with redis_client.pipeline(transaction=False) as pipe:
        for log in reqBody:
            timestamp = log.timestampMs // 1000
            key = f"rate:{timestamp}:{log.ip}"
            pipe.hincrby(key, "all", 1)
            if log.status in ("401", "404"):
                counterJson[log.status] += 1
                pipe.hincrby(key, log.status, 1)
            else: counterJson["normal"] += 1
            pipe.expire(key, 12)
        logging.info(f"Normal: {counterJson['normal']} | 401: {counterJson['401']} | 404: {counterJson['404']}")
        await pipe.execute()
