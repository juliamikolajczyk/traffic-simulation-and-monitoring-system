from uuid import UUID
import heapq
import random
import mmh3

def getUUID(userId: int, usersPerProcess: int, processId: int) -> str:
    rng = random.Random(processId * usersPerProcess + userId)
    return str(UUID(int=rng.getrandbits(128), version=4))

allowedNum1Values = tuple(set(range(1, 223 + 1)) - {10, 127, 172, 192})
def getIP(seed: str, timestampMs: int) -> str:
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

def initUsersInfo(usersCount: int) -> list:
    return [("StartSession", i) for i in range(usersCount)]

def moveFromActiveToThinking(userId: int, usersInfo: list, activeUserIds: list, thinkingUserIds: list, timestamp: int, dataJson: dict) -> None:
    elementToSwap = activeUserIds.pop()
    if elementToSwap != userId:
        activeUserIds[usersInfo[userId][1]] = elementToSwap
        usersInfo[elementToSwap] = (usersInfo[elementToSwap][0], usersInfo[userId][1])
    usersInfo[userId] = (usersInfo[userId][0], -1)
    timeRange = dataJson["operations"]["thinkingTime"][usersInfo[userId][0]]
    endOfThinkingTimestamp = timestamp + random.randint(timeRange[0], timeRange[1])
    heapq.heappush(thinkingUserIds, (endOfThinkingTimestamp, userId))

def moveFromThinkingToActive(usersInfo: list, activeUserIds: list, thinkingUserIds: list, timestampMs: int) -> None:
    while thinkingUserIds and thinkingUserIds[0][0] <= timestampMs:
        userId = heapq.heappop(thinkingUserIds)[1]
        usersInfo[userId] = (usersInfo[userId][0], len(activeUserIds))
        activeUserIds.append(userId)

def weightedDraw(weightedJson: dict) -> str:
    population = tuple(weightedJson.keys())
    weights = tuple(weightedJson.values())
    return random.choices(population, weights)[0]

def chooseOperation(userId: int, usersInfo: list, dataJson: dict) -> str:
    lastOperation = usersInfo[userId][0]
    chosenOperation = weightedDraw(dataJson["operations"]["routes"][lastOperation])
    usersInfo[userId] = (chosenOperation, usersInfo[userId][1])
    return chosenOperation
