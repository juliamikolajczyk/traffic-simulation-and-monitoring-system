import asyncio
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
import processing

infoJson = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(processing.anomaliesDetector(infoJson))
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/logs")
async def readLogs(reqBody: list[processing.log]) -> None:
    processing.processLogs(reqBody, infoJson)
    return {}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=3551, reload=True)
