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
import attack

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(processName)s | %(levelname)s | %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users-count", help="set the approximate number of users", required=True, type=int)
parser.add_argument("-l", "--url", help="url to which the logs will be sent", required=True, type=str)

def currentTimestampMs(): return int(time.time() * 1000)

async def sendLogs(session: aiohttp.ClientSession, url: str, body: list, processStatus: dict) -> None:
    processStatus["runningTasks"] += 1
    try:
        async with session.post(url, json=body) as response:
            await response.read()
        processStatus["delay"] = max(0, processStatus["delay"] - 0.1)
    except Exception as e:
        logging.error(e)
        processStatus["delay"] += 1
    finally: processStatus["runningTasks"] -= 1

async def generatorLoop(dataJson: dict, url: str, usersPerProcess: int) -> None:
    activeUserIds, thinkingUserIds = [i for i in range(usersPerProcess)], []
    usersInfo = users.initUsersInfo(usersPerProcess)
    processId = int(multiprocessing.current_process()._identity[0])
    session = aiohttp.ClientSession()
    processStatus = {"delay": 0, "runningTasks": 0}
    logsToSend = []
    timestampToSendAfter = 0
    nextAttackTimestamp = currentTimestampMs() + random.randint(30000, 300000)
    try:
        while True:
            timestampMs = currentTimestampMs()
            users.moveFromThinkingToActive(usersInfo, activeUserIds, thinkingUserIds, timestampMs)
            if not activeUserIds:
                await asyncio.sleep(0.1)
                continue
            userId = random.choice(activeUserIds)
            uuid = users.getUUID(userId, usersPerProcess, processId)
            operation = users.chooseOperation(userId, usersInfo, dataJson)
            status = users.weightedDraw(dataJson["statuses"])
            logJson = users.makeLogJson(timestampMs, uuid, users.getIP(uuid, timestampMs),
                                        operation, users.weightedDraw(dataJson["methods"]),
                                        status, dataJson["statusMessages"][status],
                                        users.getUserAgent(uuid, dataJson["userAgents"]))
            logsToSend.append(logJson)
            users.moveFromActiveToThinking(userId, usersInfo, activeUserIds, thinkingUserIds, timestampMs, dataJson)
            if timestampMs > nextAttackTimestamp:
                nextAttackTimestamp = currentTimestampMs() + random.randint(30000, 300000)
                logsToSend.append(attack.randomAttack())
            if operation == "StartSession": await asyncio.sleep(processStatus["delay"] * random.uniform(0.921, 3.7))
            if timestampMs > timestampToSendAfter and logsToSend:
                asyncio.create_task(sendLogs(session, url, logsToSend, processStatus))
                logsToSend = []
                timestampToSendAfter = timestampMs + 1000 * random.uniform(0.2, 1.37)
            await asyncio.sleep(0 if processStatus["runningTasks"] < 3 else 0.01)
    except asyncio.CancelledError: pass
    await session.close()
    tasksLeft = [task for task in asyncio.all_tasks() if task != asyncio.current_task()]
    if tasksLeft: await asyncio.gather(*tasksLeft, return_exceptions=True)    

def startGeneratorProcess(url: str, usersPerProcess: int) -> None:
    with open("data.json", "r") as file: dataJson = json.loads(file.read())
    try: asyncio.run(generatorLoop(dataJson, url, usersPerProcess))
    except Exception as e: logging.error(e)

def main() -> None:
    multiprocessing.freeze_support()
    args = parser.parse_args()
    if args.users_count <= 0: parser.error("users count must be > 0")
    usersPerProcess = math.ceil(args.users_count / multiprocessing.cpu_count())
    logging.info(f"Starting {multiprocessing.cpu_count()} processes with {usersPerProcess} users each.")
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=startGeneratorProcess, args=(args.url, usersPerProcess))
        process.start()
        processes.append(process)
    try:
        for process in processes: process.join()
    except KeyboardInterrupt: logging.info("Closing the program...")

if __name__ == "__main__": main()
