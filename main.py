import json
import uuid
import time
import argparse
import random
import mmh3
import asyncio
import multiprocessing
import aiohttp
import math

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users-count", help="set the number of users in logs", required=True, type=int)
parser.add_argument("-l", "--url", help="url to which the logs will be sent", required=True, type=str)
args = parser.parse_args()
if args.users_count <= 0: parser.error("users count must be > 0")

def generateUserIds(amount: int) -> tuple:
    return tuple(str(uuid.uuid4()) for _ in range(amount))

allowedNum1Values = tuple(set(range(1, 223 + 1)) - {10, 127, 172, 192})
def generateIP(seed: str, timestampMs: int) -> str:
    hash = mmh3.hash(seed)
    hash = hash + (timestampMs) // (1000 * 60 * (abs(hash) % 450 + 30)) # time window from 30mins to 8hrs
    num1 = allowedNum1Values[hash % len(allowedNum1Values)]
    num2 = hash % 256
    num3 = (hash >> 8) % 256
    num4 = (hash >> 16) % 256
    return f"{num1}.{num2}.{num3}.{num4}"

with open("data.json", "r") as file:
    dataJson = json.loads(file.read())

userIdsCountPerProcess = math.ceil(args.users_count / multiprocessing.cpu_count())
methods = tuple(dataJson["methods"].keys())
methodsWeights = tuple(dataJson["methods"].values())
statuses = tuple(dataJson["statuses"].keys())
statusesWeights = tuple(dataJson["statuses"].values())

async def sendLogs(session: aiohttp.ClientSession, url: str, body: dict) -> None:
    try:
        async with session.post(url, json=body) as response:
            await response.read()
    except Exception as e: print(f"Error: {e}")

async def generatorLoop() -> None:
    userIds = generateUserIds(userIdsCountPerProcess)
    session = aiohttp.ClientSession()
    try:
        while True:
            logJson = {
                "timestampMs": int(time.time() * 1000),
                "userId": random.choice(userIds),
                "ip": None,
                "operation": random.choice(dataJson["operations"]),
                "method": random.choices(population=methods, weights=methodsWeights)[0],
                "status": random.choices(population=statuses, weights=statusesWeights)[0],
                "message": None,
                "userAgent": random.choice(dataJson["userAgents"])
            }
            logJson["ip"] = generateIP(logJson["userId"], logJson["timestampMs"])
            logJson["message"] = dataJson["statusMessages"][logJson["status"]]
            asyncio.create_task(sendLogs(session, args.url, logJson))
            await asyncio.sleep(random.uniform(0.01, 0.05))
    except asyncio.CancelledError: pass
    await session.close()
    tasksLeft = [task for task in asyncio.all_tasks() if task != asyncio.current_task()]
    if tasksLeft: await asyncio.gather(*tasksLeft, return_exceptions=True)    

def startGeneratorProcess() -> None:
    try: asyncio.run(generatorLoop())
    except: pass

if __name__ == "__main__":
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=startGeneratorProcess)
        process.start()
        processes.append(process)
    try:
        for process in processes: process.join()
    except KeyboardInterrupt: pass
