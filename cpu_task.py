import time
import threading


def cpu_heavy_task(n: int = 35_000_000) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def run_threads(thread_count: int = 4, n: int = 35_000_000):
    start = time.perf_counter()

    results = []

    def worker():
        results.append(cpu_heavy_task(n))

    threads = []

    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.perf_counter()

    return {
        "thread_count": thread_count,
        "duration_seconds": round(end - start, 2),
        "result_count": len(results),
    }


def queue_cpu_job(job_id: str, n: int = 35_000_000):
    start = time.perf_counter()
    result = cpu_heavy_task(n)
    end = time.perf_counter()

    return {
        "job_id": job_id,
        "duration_seconds": round(end - start, 2),
        "result": result,
    }
