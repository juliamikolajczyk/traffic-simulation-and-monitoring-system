import json
import time
import argparse
import random
import asyncio
import multiprocessing
import aiohttp
import math
import logging
import users

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(processName)s | %(levelname)s | %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users-count", help="set the approximate number of users", required=True, type=int)
parser.add_argument("-l", "--url", help="url to which the logs will be sent", required=True, type=str)
args = parser.parse_args()
if args.users_count <= 0: parser.error("users count must be > 0")
userIdsCountPerProcess = math.ceil(args.users_count / multiprocessing.cpu_count())

with open("data.json", "r") as file: dataJson = json.loads(file.read())

async def sendLogs(session: aiohttp.ClientSession, url: str, body: dict, delayVal: list) -> None:
    try:
        async with session.post(url, json=body) as response:
            await response.read()
        delayVal[0] = max(0, delayVal[0] - 0.1)
    except Exception as e:
        delayVal[0] += 1
        logging.error(e)

async def generatorLoop() -> None:
    activeUserIds, thinkingUserIds = users.generateUserIds(userIdsCountPerProcess), []
    usersJson = users.initUsersJson(activeUserIds)
    session = aiohttp.ClientSession()
    delayVal = [0]
    try:
        while True:
            timestampMs = int(time.time() * 1000)
            users.moveFromThinkingToActive(usersJson, activeUserIds, thinkingUserIds, timestampMs)
            if not activeUserIds:
                await asyncio.sleep(0.1)
                continue
            userId = random.choice(activeUserIds)
            operation = users.chooseOperation(userId, usersJson, dataJson)
            status = users.weightedDraw(dataJson["statuses"])
            logJson = {
                "timestampMs": timestampMs,
                "userId": userId,
                "ip": users.generateIP(userId, timestampMs),
                "operation": operation,
                "method": users.weightedDraw(dataJson["methods"]),
                "status": status,
                "message": dataJson["statusMessages"][status],
                "userAgent": random.choice(dataJson["userAgents"])
            }
            users.moveFromActiveToThinking(userId, usersJson, activeUserIds, thinkingUserIds, timestampMs, dataJson)
            if operation == "StartSession": await asyncio.sleep(delayVal[0] * random.uniform(0.921, 3.7))
            asyncio.create_task(sendLogs(session, args.url, logJson, delayVal))
            await asyncio.sleep(random.uniform(0.01, 0.05))
    except asyncio.CancelledError: pass
    await session.close()
    tasksLeft = [task for task in asyncio.all_tasks() if task != asyncio.current_task()]
    if tasksLeft: await asyncio.gather(*tasksLeft, return_exceptions=True)    

def startGeneratorProcess() -> None:
    try: asyncio.run(generatorLoop())
    except Exception as e: logging.error(e)

if __name__ == "__main__":
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=startGeneratorProcess)
        process.start()
        processes.append(process)
    try:
        for process in processes: process.join()
    except KeyboardInterrupt: logging.info("Closing the program...")
