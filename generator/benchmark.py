import sys
import psutil
from pathlib import Path
from time import sleep, time

def writeToFile(path: str, content: str) -> None:
    with open(path, "a") as file: file.write(content)

def main():
    generatorPath = str(Path(__file__).parent / "main.py")
    mainProcess = psutil.Popen([sys.executable, generatorPath, "-u", "10000000", "-l", "http://127.0.0.1:3551/logs"])

    csvPath = str(Path(__file__).parent / f"benchmark_{int(time())}.csv")
    writeToFile(csvPath, "Time;RAM\n")

    seconds = 0

    while mainProcess.is_running():
        subprocesses = mainProcess.children()
        totalRamUsed = mainProcess.memory_info().rss
        for process in subprocesses:
            try: totalRamUsed += process.memory_info().rss
            except: pass
        writeToFile(csvPath, f"{seconds};{totalRamUsed // (1024 * 1024)}\n")
        seconds += 1
        sleep(1)

if __name__ == "__main__": main()
