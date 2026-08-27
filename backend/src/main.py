import asyncio
from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager
import processing
from collections import defaultdict
from redis.asyncio import Redis
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis(host=os.environ["REDIS_HOST"], port=6379, decode_responses=True)
    asyncio.create_task(processing.anomaliesDetectorLoop(redis_client))
    yield {"redis_client": redis_client}

app = FastAPI(lifespan=lifespan)

@app.post("/logs")
async def readLogs(req: Request, reqBody: list[processing.Log]) -> None:
    await processing.processLogs(reqBody, req.state.redis_client)
    return {}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reload=False)
