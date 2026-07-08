import json
import uuid
import time
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users-count", help="set the number of users in logs", required=True, type=int)
parser.add_argument("-r", "--rate", help="set the rate multiplier of logs generation", default=1, type=float)
args = parser.parse_args()
if args.users_count <= 0 or args.rate <= 0: parser.error("arg values must be > 0")

def generateUserIds(amount):
    return [str(uuid.uuid4()) for _ in range(amount)]

def generateIPs(amount):
    ipList = []
    forbiddenNumbers = {10, 127, 172, 192}
    for _ in range(amount):
        num1 = random.randint(1, 223)
        while num1 in forbiddenNumbers:
            num1 = random.randint(1, 223)
        num2 = random.randint(0, 255)
        num3 = random.randint(0, 255)
        num4 = random.randint(0, 255)
        ipList.append(f"{num1}.{num2}.{num3}.{num4}")
    return ipList

def assignIPsToUserIds(userIds, ipList):
    jsonToReturn = {}
    multipleIPsUserIds = set(random.sample(userIds, int(len(userIds) * 0.02)))
    for userId in userIds:
        if userId in multipleIPsUserIds:
            jsonToReturn[userId] = tuple(random.sample(ipList, random.randint(2, 7)))
        else: jsonToReturn[userId] = tuple([random.choice(ipList)])
    return jsonToReturn

with open("data.json", "r") as file:
    dataJson = json.loads(file.read())

userIds = generateUserIds(args.users_count)
ipList = generateIPs(args.users_count)
userIPsJson = assignIPsToUserIds(userIds, ipList)
while True:
    userId = random.choice(userIds)
    logJson = {
        "timestamp": int(time.time()),
        "userId": userId,
        "ip": random.choice(userIPsJson[userId]),
        "operation": random.choice(dataJson["operations"]),
        "method": random.choice(dataJson["methods"]),
        "status": 200,
        "message": "OK",
        "userAgent": random.choice(dataJson["userAgents"])
    }
    print(json.dumps(logJson))
    time.sleep(random.uniform(0.01, 0.1) / args.rate)
    # send json stuff
