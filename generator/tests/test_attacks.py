import attacks

def get_mock_json():
    return {
        "statuses": {"200": 100},
        "operations": {
            "list": ["testoperation"]
        },
        "methods": {"GET": 100},
        "statusMessages": {
            "200": "OK",
            "401": "Unauthorized",
            "404": "Not Found"
        },
        "userAgents": ["testagent"]
    }

def test_next_attack_timestamp():
    timestampMs = attacks.getNextAttackTimestamp(1)

    assert isinstance(timestampMs, int)

    assert timestampMs > 30000

def test_operation_tester():
    mockJson = get_mock_json()
    logJson = attacks.nonexistingOperationTester(mockJson)
    accountIds = set()
    for log in logJson:
        accountIds.add(log["accountId"])

        assert log["status"] == "404"

        assert log["operation"] not in mockJson["operations"]["list"]

        assert 3 <= len(log["operation"]) and len(log["operation"]) <= 12

    assert len(accountIds) == 1

def test_dos():
    mockJson = get_mock_json()
    logJson = attacks.DOS(mockJson)
    ips = set()
    for log in logJson:
        ips.add(log["ip"])
    assert len(ips) == 1

def test_brute_force():
    mockJson = get_mock_json()
    logJson = attacks.bruteForce(mockJson)
    accountIds, ips = set(), set()
    for log in logJson:
        accountIds.add(log["accountId"])
        ips.add(log["ip"])

        assert log["status"] == "401"
        assert log["operation"] == "ClientLogin"

    assert len(accountIds) == len(ips) == 1


def test_random_attack():
    mockJson = get_mock_json()
    logJson = attacks.makeRandomAttack(mockJson)

    assert isinstance(logJson, list)
    assert len(logJson) == 10
