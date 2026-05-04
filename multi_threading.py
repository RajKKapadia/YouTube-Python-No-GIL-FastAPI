import threading
import time
import os

def worker(name, sleep_time):
    print(f"{name} started | PID: {os.getpid()}")
    time.sleep(sleep_time)
    print(f"{name} finished after {sleep_time}s")

if __name__ == "__main__":
    print(f"Main process PID: {os.getpid()}")

    threads = []

    for i in range(3):
        t = threading.Thread(target=worker, args=(f"Thread-{i}", 10))
        threads.append(t)
        t.start()

    print("Main thread continues...")

    for t in threads:
        t.join()

    print("All threads finished")
