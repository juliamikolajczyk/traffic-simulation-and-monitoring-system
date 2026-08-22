import time
import asyncio
from pydantic import BaseModel
from collections import defaultdict
import detection

class log(BaseModel):
    timestampMs: int
    accountId: str
    ip: str
    operation: str
    method: str
    status: str
    message: str
    userAgent: str

def clearOldLogs(infoJson: dict, jsonTimestamp: int, currentTimestamp: int) -> bool:
    if jsonTimestamp + 12 < currentTimestamp:
        del infoJson[jsonTimestamp]
        return True
    return False

def buildCounterJson(infoJson: dict, jsonTimestamp: int, currentTimestamp: int, counterJson: dict) -> None:
    if jsonTimestamp + 10 >= currentTimestamp:
        for ip in infoJson[jsonTimestamp]:
            for i in range(3):
                counterJson[ip][i] += infoJson[jsonTimestamp][ip][i]

async def anomaliesDetectorLoop(infoJson: dict) -> None:
    while True:
        counterJson = defaultdict(lambda: [0, 0, 0])
        currentTimestamp = int(time.time())
        for timestamp in tuple(infoJson.keys()):
            if clearOldLogs(infoJson, timestamp, currentTimestamp): continue
            buildCounterJson(infoJson, timestamp, currentTimestamp, counterJson)
        detection.runAllFunctions(counterJson)
        await asyncio.sleep(0.9)

def processLogs(reqBody: list[log], infoJson: dict) -> None:
    countAll, count401, count404 = [0, 1, 2]
    for log in reqBody:
        timestamp = log.timestampMs // 1000
        jsonPath = infoJson[timestamp][log.ip]
        jsonPath[countAll] += 1
        if log.status == "401": jsonPath[count401] += 1
        elif log.status == "404": jsonPath[count404] += 1
