from multiprocessing import Process
import os
import time

def worker(name, sleep_time):
    print(f"{name} started | PID: {os.getpid()}")
    time.sleep(sleep_time)
    print(f"{name} finished after {sleep_time}s")

if __name__ == "__main__":
    print(f"Main process PID: {os.getpid()}")

    processes = []

    # Create 3 processes with different sleep times
    for i in range(3):
        p = Process(target=worker, args=(f"Worker-{i}", 10))
        processes.append(p)
        p.start()

    print("Main process continues...")

    for p in processes:
        p.join()

    print("All processes finished")