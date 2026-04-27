from fastapi import FastAPI
from redis import Redis
from rq import Queue
from cpu_task import run_threads, queue_cpu_job
import uuid

app = FastAPI()

redis_conn = Redis(host="localhost", port=6379, db=0)
queue = Queue("cpu-jobs", connection=redis_conn)


@app.get("/")
def home():
    return {
        "message": "FastAPI GIL demo",
        "endpoints": [
            "/thread-test?threads=4",
            "/queue-job",
            "/job/{job_id}",
        ],
    }


@app.get("/thread-test")
def thread_test(threads: int = 4):
    """
    CPU-heavy work inside FastAPI using Python threads.

    Normal Python:
      - GIL prevents true parallel execution of Python bytecode.

    Free-threaded Python:
      - Threads can run in parallel.
    """
    return run_threads(thread_count=threads)


@app.post("/queue-job")
def create_queue_job():
    """
    Push CPU-heavy work to Redis Queue.

    This is the production-style approach:
    FastAPI returns quickly.
    Worker does the heavy work separately.
    """
    job_id = str(uuid.uuid4())

    job = queue.enqueue(
        queue_cpu_job,
        job_id,
        job_timeout=600,
    )

    return {
        "status": "queued",
        "job_id": job.id,
        "custom_job_id": job_id,
    }


@app.get("/job/{job_id}")
def get_job(job_id: str):
    job = queue.fetch_job(job_id)

    if job is None:
        return {"status": "not_found"}

    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result,
    }
