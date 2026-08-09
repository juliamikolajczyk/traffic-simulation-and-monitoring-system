import users
import random

def getNextAttackTimestamp(currentTimestampMs: int) -> int:
    return currentTimestampMs + random.randint(30000, 300000)

def nonexistingOperationTester(dataJson: dict) -> list:
    logs = []
    timestampMs = users.getTimestampMs()
    accountId = users.getId()
    for _ in range(10):
        operation = users.getId()[0:random.randint(3, 12)]
        logs.append(users.makeLogJson(
            timestampMs=timestampMs,
            accountId=accountId,
            operation=operation,
            status="404",
            dataJson=dataJson
        ))
        timestampMs -= random.randint(256, 997)
    return logs

def DOS(dataJson: dict) -> list:
    logs = []
    timestampMs = users.getTimestampMs()
    ip = users.getIP(hex(timestampMs), timestampMs)
    for _ in range(10):
        logs.append(users.makeLogJson(
            timestampMs=timestampMs,
            ip=ip,
            dataJson=dataJson
        ))
        timestampMs -= random.randint(256, 997)
    return logs

def makeRandomAttack(dataJson: dict) -> list:
    functions = [
        nonexistingOperationTester,
        DOS
    ]
    return random.choice(functions)(dataJson)
