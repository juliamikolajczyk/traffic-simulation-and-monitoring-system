import users
import random
from uuid import uuid4

def nonexistingOperationTester():
    accountId = str(uuid4())
    operation = accountId.replace("-", "")[0:random.randint(3, 30)]
    return users.makeLogJson(accountId=accountId, operation=operation, status="404", message="Not Found")

def randomAttack():
    return nonexistingOperationTester()
