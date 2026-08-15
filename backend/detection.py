def dos(counterJson: dict) -> None:
    for ip in counterJson:
        if counterJson[ip] > 10: print(f"Warn DOS from IP: {ip}")

def runAllFunctions(counterJson: dict) -> None:
    dos(counterJson)
