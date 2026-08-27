import users

def test_timestamp():
    timestampMs = users.getTimestampMs()
    assert isinstance(timestampMs, int)


def test_id_format():
    ids = (users.getId(), users.getId(2, 13, 7))
    for id in ids:
        assert isinstance(id, str)

        assert 0 < len(id) and len(id) <= 32

        assert all(i in "0123456789abcdef" for i in id)

    assert ids[0] != ids[1]


def test_ip_format():
    for _ in range(10):
        ip = users.getIP(users.getId(), users.getTimestampMs())

        assert isinstance(ip, str)

        ipSplit = ip.split(".")
        assert len(ipSplit) == 4

        for number in ipSplit:
            assert number.isdigit()

            numberInt = int(number)
            assert 0 <= numberInt and numberInt <= 255

        num1 = int(ipSplit[0])
        assert 1 <= num1 and num1 <= 223
        assert num1 not in (10, 127, 172, 192)


def test_user_agent():
    id = users.getId()
    agents = ["a", "b", "c", "z"]
    userAgent = users.getUserAgent(id, agents)

    assert isinstance(userAgent, str)

    assert userAgent in agents


def test_users_info():
    info = users.initUsersInfo(22)
    idCounter = 0
    for operation, id in info:
        assert operation == "StartSession"

        assert id == idCounter
        idCounter += 1


def test_active_to_thinking():
    mockJson = {
        "operations": {
            "thinkingTime": {
                "StartSession": [1000, 3000]
            }
        }
    }
    usersCount = 10
    userId = 5
    usersInfo = users.initUsersInfo(usersCount)
    activeUserIds, thinkingUserIds = [i for i in range(usersCount)], []
    timestampMs = users.getTimestampMs()

    users.moveFromActiveToThinking(userId, usersInfo, activeUserIds, thinkingUserIds, timestampMs, mockJson)

    assert usersInfo[userId][1] == -1
    assert userId not in activeUserIds
    assert len(activeUserIds) == usersCount - 1
    assert len(thinkingUserIds) == 1


def test_thinking_to_active():
    mockJson = {
        "operations": {
            "thinkingTime": {
                "StartSession": [1, 2]
            }
        }
    }
    usersCount = 10
    usersInfo = users.initUsersInfo(usersCount)
    activeUserIds, thinkingUserIds = [i for i in range(usersCount)], []
    timestampMs = users.getTimestampMs()

    for userId in range(usersCount - 1):
        users.moveFromActiveToThinking(userId, usersInfo, activeUserIds, thinkingUserIds, timestampMs, mockJson)

    users.moveFromThinkingToActive(usersInfo, activeUserIds, thinkingUserIds, timestampMs + 1000)

    assert len(thinkingUserIds) == 0
    assert len(activeUserIds) == usersCount

    for userId in range(usersCount):
        assert usersInfo[userId][1] != -1


def test_weighted_draw():
    weightedJson = {
        "test1": 50,
        "test2": 20,
        "test3": 15,
        "test4": 10,
        "test5": 5
    }

    draw = users.weightedDraw(weightedJson)

    assert isinstance(draw, str)

    assert draw in weightedJson.keys()


def test_choose_operation():
    mockJson = {
        "operations": {
            "routes": {
                "StartSession": {
                    "ClientLogin": 100
                }
            }
        }
    }
    usersCount = 20
    usersInfo = users.initUsersInfo(usersCount)

    operation = users.chooseOperation(3, usersInfo, mockJson)
    assert operation == "ClientLogin"

    assert usersInfo[3] == ("ClientLogin", 3)


def test_log_json():
    mockJson = {
        "statuses": {"200": 100},
        "operations": {
            "list": ["ClientRegister"]
        },
        "methods": {"GET": 100},
        "statusMessages": {"200": "OK"},
        "userAgents": ["testagent"]
    }
    log = users.makeLogJson(dataJson=mockJson)
    assert isinstance(log, dict)

    keys = ("timestampMs", "accountId", "ip", "operation", "method", "status", "message", "userAgent")

    for key in keys:
        assert key in log
    
    for key in log:
        assert key in keys
