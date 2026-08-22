import asyncio
from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager
import processing
from collections import defaultdict

@asynccontextmanager
async def lifespan(app: FastAPI):
    infoJson = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    asyncio.create_task(processing.anomaliesDetectorLoop(infoJson))
    yield {"infoJson": infoJson}

app = FastAPI(lifespan=lifespan)

@app.post("/logs")
async def readLogs(req: Request, reqBody: list[processing.log]) -> None:
    processing.processLogs(reqBody, req.state.infoJson)
    return {}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=3551, reload=True)
