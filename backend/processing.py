import time
import asyncio
from pydantic import BaseModel

class log(BaseModel):
    timestampMs: int
    accountId: str
    ip: str
    operation: str
    method: str
    status: str
    message: str
    userAgent: str

def cleanOldLogs(infoJson: dict, jsonTimestamp: int, currentTimestamp: int) -> bool:
    if jsonTimestamp + 12 < currentTimestamp:
        del infoJson[jsonTimestamp]
        return True
    return False

def buildCurrentJson(infoJson: dict, jsonTimestamp: int, currentTimestamp: int, currentJson: dict) -> bool:
    if jsonTimestamp + 10 >= currentTimestamp:
        for ip in infoJson[jsonTimestamp]:
            if not ip in currentJson: currentJson[ip] = 0
            currentJson[ip] += infoJson[jsonTimestamp][ip]

async def anomaliesDetector(infoJson: dict) -> None:
    while True:
        currentJson = {}
        currentTimestamp = int(time.time())
        for timestamp in tuple(infoJson.keys()):
            if cleanOldLogs(infoJson, timestamp, currentTimestamp): continue
            buildCurrentJson(infoJson, timestamp, currentTimestamp, currentJson)
        for ip in currentJson:
            if currentJson[ip] > 10: print(f"Warn DOS from IP: {ip}")
        await asyncio.sleep(0.9)

def processLogs(reqBody: list[log], infoJson: dict) -> None:
    for log in reqBody:
        timestamp = log.timestampMs // 1000
        if not timestamp in infoJson: infoJson[timestamp] = {}
        if not log.ip in infoJson[timestamp]: infoJson[timestamp][log.ip] = 0
        infoJson[timestamp][log.ip] += 1
