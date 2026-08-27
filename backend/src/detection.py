import logging

def detect(counterJson: dict) -> None:
    indexToMessage = ["DOS", "brute force", "non-existing operation tester"]
    for ip in counterJson:
        for i in range(3):
            if counterJson[ip][i] >= 10:
                logging.warning(f"Warn {indexToMessage[i]} from {ip}")

def runAllFunctions(counterJson: dict) -> None:
    detect(counterJson)
