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
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users-count", help="set the number of users in logs", required=True, type=int)
parser.add_argument("-l", "--url", help="url to which the logs will be sent", required=True, type=str)
args = parser.parse_args()
if args.users_count <= 0: parser.error("users count must be > 0")

def generateUserIds(amount: int) -> list:
    return [str(uuid.uuid4()) for _ in range(amount)]

def initUsersJson(userIds: tuple) -> dict:
    usersJson = {}
    indexCounter = 0
    for userId in userIds:
        usersJson[userId] = ("StartSession", indexCounter)
        indexCounter += 1
    return usersJson

def moveFromActiveToThinking(userId: str, usersJson: dict, activeUserIds: list, thinkingUserIds: list, newTimestamp: int) -> None:
    elementToSwap = activeUserIds.pop()
    if elementToSwap != userId:
        activeUserIds[usersJson[userId][1]] = elementToSwap
        usersJson[elementToSwap] = (usersJson[elementToSwap][0], usersJson[userId][1])
    usersJson[userId] = (usersJson[userId][0], -1)
    heapq.heappush(thinkingUserIds, (newTimestamp, userId))

def moveFromThinkingToActive(usersJson: dict, activeUserIds: list, thinkingUserIds: list) -> None:
    userId = heapq.heappop(thinkingUserIds)[1]
    usersJson[userId] = (usersJson[userId][0], len(activeUserIds))
    activeUserIds.append(userId)

def chooseOperation(userId: str, usersJson: dict) -> str:
    lastOperation = usersJson[userId][0]
    operations = tuple(dataJson["operations"][lastOperation].keys())
    operationsWeights = tuple(dataJson["operations"][lastOperation].values())
    chosenOperation = random.choices(population=operations, weights=operationsWeights)[0]
    usersJson[userId] = (chosenOperation, usersJson[userId][1])
    return chosenOperation

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
    activeUserIds, thinkingUserIds = generateUserIds(userIdsCountPerProcess), []
    usersJson = initUsersJson(activeUserIds)
    session = aiohttp.ClientSession()
    try:
        while True:
            timestampMs = int(time.time() * 1000)
            while thinkingUserIds and thinkingUserIds[0][0] <= timestampMs:
                moveFromThinkingToActive(usersJson, activeUserIds, thinkingUserIds)
            if not activeUserIds:
                await asyncio.sleep(0.1)
                continue
            userId = random.choice(activeUserIds)
            logJson = {
                "timestampMs": timestampMs,
                "userId": userId,
                "ip": None,
                "operation": None,
                "method": random.choices(population=methods, weights=methodsWeights)[0],
                "status": random.choices(population=statuses, weights=statusesWeights)[0],
                "message": None,
                "userAgent": random.choice(dataJson["userAgents"])
            }
            logJson["ip"] = generateIP(logJson["userId"], logJson["timestampMs"])
            logJson["operation"] = chooseOperation(logJson["userId"], usersJson)
            logJson["message"] = dataJson["statusMessages"][logJson["status"]]
            timeRange = dataJson["operations"]["thinkingTime"][logJson["operation"]]
            thinkingTime = random.randint(timeRange[0], timeRange[1])
            moveFromActiveToThinking(userId, usersJson, activeUserIds, thinkingUserIds, timestampMs + thinkingTime)
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
