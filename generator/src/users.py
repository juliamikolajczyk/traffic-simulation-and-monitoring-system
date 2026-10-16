import time
import heapq
import random
import mmh3

def getTimestampMs(): return int(time.time() * 1000)

def getId(userId: int = None, usersPerProcess: int = None, processId: int = None) -> str:
    base = getTimestampMs()
    if userId is not None and usersPerProcess is not None and processId is not None:
        base += processId * usersPerProcess + userId
    hashInt = mmh3.hash128((base).to_bytes(8, "little"))
    return hex(hashInt)[2:]

allowedNum1Values = tuple(set(range(1, 223 + 1)) - {10, 127, 172, 192})
def getIP(seed: str, timestampMs: int) -> str:
    hashInt = mmh3.hash(seed)
    hashInt = hashInt + (timestampMs) // (1000 * 60 * (abs(hashInt) % 450 + 30)) # time window from 30mins to 8hrs
    num1 = allowedNum1Values[hashInt % len(allowedNum1Values)]
    num2 = hashInt % 256
    num3 = (hashInt >> 8) % 256
    num4 = (hashInt >> 16) % 256
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

def makeLogJson(timestampMs: int = None, accountId: str = None, ip: str = None,
                operation: str = None, method: str = None, status: str = None,
                message: str = None, userAgent: str = None, dataJson: dict = None) -> dict:
    if timestampMs is None: timestampMs = getTimestampMs()
    if accountId is None: accountId = getId()
    if status is None: status = weightedDraw(dataJson["statuses"])
    return {
        "timestampMs": timestampMs,
        "accountId": accountId,
        "ip": ip if ip is not None else getIP(accountId, timestampMs),
        "operation": operation if operation is not None else random.choice(dataJson["operations"]["list"]),
        "method": method if method is not None else weightedDraw(dataJson["methods"]),
        "status": status,
        "message": message if message is not None else dataJson["statusMessages"][status],
        "userAgent": userAgent if userAgent is not None else getUserAgent(accountId, dataJson["userAgents"])
    }
