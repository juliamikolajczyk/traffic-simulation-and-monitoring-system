import time
import asyncio
from pydantic import BaseModel
from collections import defaultdict

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
            counterJson[ip] += infoJson[jsonTimestamp][ip]

async def anomaliesDetectorLoop(infoJson: dict) -> None:
    while True:
        counterJson = defaultdict(int)
        currentTimestamp = int(time.time())
        for timestamp in tuple(infoJson.keys()):
            if clearOldLogs(infoJson, timestamp, currentTimestamp): continue
            buildCounterJson(infoJson, timestamp, currentTimestamp, counterJson)
        for ip in counterJson:
            if counterJson[ip] > 10: print(f"Warn DOS from IP: {ip}")
        await asyncio.sleep(0.9)

def processLogs(reqBody: list[log], infoJson: dict) -> None:
    for log in reqBody:
        timestamp = log.timestampMs // 1000
        infoJson[timestamp][log.ip] += 1
