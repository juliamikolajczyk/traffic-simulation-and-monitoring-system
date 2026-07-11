import json
import uuid
import time
import argparse
import random
import mmh3
import asyncio
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users-count", help="set the number of users in logs", required=True, type=int)
parser.add_argument("-r", "--rate", help="set the rate multiplier of logs generation", default=1, type=float)
args = parser.parse_args()
if args.users_count <= 0 or args.rate <= 0: parser.error("arg values must be > 0")

def generateUserIds(amount):
    return [str(uuid.uuid4()) for _ in range(amount)]

allowedNum1Values = tuple(set(range(1, 223 + 1)) - {10, 127, 172, 192})
def generateIP(seed, timestamp):
    hash = mmh3.hash(seed)
    hash = hash + (timestamp) // (1000 * 60 * (abs(hash) % 450 + 30)) # time window from 30mins to 8hrs
    num1 = allowedNum1Values[hash % len(allowedNum1Values)]
    num2 = hash % 256
    num3 = (hash >> 8) % 256
    num4 = (hash >> 16) % 256
    return f"{num1}.{num2}.{num3}.{num4}"

with open("data.json", "r") as file:
    dataJson = json.loads(file.read())

userIds = generateUserIds(args.users_count)
methods = tuple(dataJson["methods"].keys())
methodsWeights = tuple(dataJson["methods"].values())
statuses = tuple(dataJson["statuses"].keys())
statusesWeights = tuple(dataJson["statuses"].values())

def generatorLoop():
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
            #print(json.dumps(logJson))
            #time.sleep(random.uniform(0.01, 0.1) / args.rate)
            # send json stuff
    except KeyboardInterrupt: []

if __name__ == "__main__":
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=generatorLoop)
        process.start()
        processes.append(process)
    try:
        for process in processes: process.join()
    except KeyboardInterrupt: []
