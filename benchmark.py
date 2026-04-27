import asyncio
import time
import httpx


BASE_URL = "http://localhost:8000"


async def hit_thread_test(client: httpx.AsyncClient, threads: int = 4):
    response = await client.get(f"{BASE_URL}/thread-test?threads={threads}", timeout=300)
    return response.json()


async def hit_queue_job(client: httpx.AsyncClient):
    response = await client.post(f"{BASE_URL}/queue-job", timeout=30)
    return response.json()


async def benchmark_thread_endpoint(requests: int = 4, threads_per_request: int = 4):
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        tasks = [
            hit_thread_test(client, threads=threads_per_request)
            for _ in range(requests)
        ]

        results = await asyncio.gather(*tasks)

    end = time.perf_counter()

    print("\nTHREAD ENDPOINT BENCHMARK")
    print("-------------------------")
    print(f"Requests: {requests}")
    print(f"Threads per request: {threads_per_request}")
    print(f"Total duration: {round(end - start, 2)} seconds")

    for result in results:
        print(result)


async def benchmark_queue_endpoint(requests: int = 8):
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        tasks = [hit_queue_job(client) for _ in range(requests)]
        results = await asyncio.gather(*tasks)

    end = time.perf_counter()

    print("\nQUEUE ENDPOINT BENCHMARK")
    print("------------------------")
    print(f"Queued jobs: {requests}")
    print(f"API response duration: {round(end - start, 2)} seconds")

    for result in results:
        print(result)


async def main():
    await benchmark_thread_endpoint(requests=4, threads_per_request=4)
    await benchmark_queue_endpoint(requests=8)


if __name__ == "__main__":
    asyncio.run(main())
    