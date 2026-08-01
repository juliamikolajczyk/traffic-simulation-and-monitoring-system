from uuid import uuid4
import heapq
import random
import mmh3

def generateUserIds(amount: int) -> list:
    return [str(uuid4()) for _ in range(amount)]

def initUsersJson(userIds: tuple) -> dict:
    usersJson = {}
    indexCounter = 0
    for userId in userIds:
        usersJson[userId] = ("StartSession", indexCounter)
        indexCounter += 1
    return usersJson

def moveFromActiveToThinking(userId: str, usersJson: dict, activeUserIds: list, thinkingUserIds: list, timestamp: int, dataJson: dict) -> None:
    elementToSwap = activeUserIds.pop()
    if elementToSwap != userId:
        activeUserIds[usersJson[userId][1]] = elementToSwap
        usersJson[elementToSwap] = (usersJson[elementToSwap][0], usersJson[userId][1])
    usersJson[userId] = (usersJson[userId][0], -1)
    timeRange = dataJson["operations"]["thinkingTime"][usersJson[userId][0]]
    endOfThinkingTimestamp = timestamp + random.randint(timeRange[0], timeRange[1])
    heapq.heappush(thinkingUserIds, (endOfThinkingTimestamp, userId))

def moveFromThinkingToActive(usersJson: dict, activeUserIds: list, thinkingUserIds: list, timestampMs: int) -> None:
    while thinkingUserIds and thinkingUserIds[0][0] <= timestampMs:
        userId = heapq.heappop(thinkingUserIds)[1]
        usersJson[userId] = (usersJson[userId][0], len(activeUserIds))
        activeUserIds.append(userId)

def weightedDraw(weightedJson: dict) -> str:
    population = tuple(weightedJson.keys())
    weights = tuple(weightedJson.values())
    return random.choices(population, weights)[0]

def chooseOperation(userId: str, usersJson: dict, dataJson: dict) -> str:
    lastOperation = usersJson[userId][0]
    chosenOperation = weightedDraw(dataJson["operations"]["routes"][lastOperation])
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

def getUserAgent(seed: str, userAgents: list) -> str:
    hash = mmh3.hash(seed)
    return userAgents[abs(hash) % len(userAgents)]
