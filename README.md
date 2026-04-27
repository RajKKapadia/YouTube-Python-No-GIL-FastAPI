# Python No-GIL FastAPI Demo

This project demonstrates two ways to handle CPU-heavy work from a FastAPI app:

- Running CPU-bound work directly in Python threads through a request handler.
- Offloading CPU-bound work to a Redis Queue worker so the API can return quickly.

It is designed for comparing normal Python behavior with a free-threaded Python build where the GIL is disabled.

## Project Structure

- `app.py` - FastAPI application and HTTP endpoints.
- `cpu_task.py` - CPU-heavy task plus threaded and queued execution helpers.
- `worker.py` - RQ worker process for jobs in the `cpu-jobs` queue.
- `benchmark.py` - Async benchmark script that calls the API endpoints concurrently.
- `pyproject.toml` - Project metadata and dependencies for `uv`.
- `requirements.txt` - Exported dependency list for `pip`.

## Requirements

- Python 3.13.7 or newer
- Redis running on `localhost:6379`
- Either `uv` or `pip`

## Setup

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start Redis if it is not already running:

```bash
redis-server
```

Or run Redis with Docker:

```bash
docker run --rm --name fastapi-gil-redis -p 6379:6379 redis:7
```

## Run The API

```bash
uv run uvicorn app:app --reload
```

Or, if you installed with `pip`:

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## Run The Worker

The queue endpoint needs a separate worker process:

```bash
uv run python worker.py
```

Or, with an activated virtual environment:

```bash
python worker.py
```

## Endpoints

### `GET /`

Returns a short list of available endpoints.

### `GET /thread-test?threads=4`

Runs CPU-heavy work inside the FastAPI process using Python threads.

Example:

```bash
curl "http://localhost:8000/thread-test?threads=4"
```

Response shape:

```json
{
  "thread_count": 4,
  "duration_seconds": 12.34,
  "result_count": 4
}
```

### `POST /queue-job`

Queues CPU-heavy work in Redis Queue and returns immediately with the queued job id.

Example:

```bash
curl -X POST "http://localhost:8000/queue-job"
```

Response shape:

```json
{
  "status": "queued",
  "job_id": "rq-job-id",
  "custom_job_id": "generated-job-id"
}
```

### `GET /job/{job_id}`

Checks the status and result of an RQ job.

Example:

```bash
curl "http://localhost:8000/job/rq-job-id"
```

Response shape:

```json
{
  "job_id": "rq-job-id",
  "status": "finished",
  "result": {
    "job_id": "generated-job-id",
    "duration_seconds": 3.21,
    "result": 14291666041244791667500000
  }
}
```

## Run The Benchmark

Start Redis, the API server, and the worker first. Then run:

```bash
uv run python benchmark.py
```

Or, with an activated virtual environment:

```bash
python benchmark.py
```

The benchmark sends concurrent requests to:

- `/thread-test?threads=4`
- `/queue-job`

Use the printed durations to compare direct threaded work against queue-based offloading.

## Notes

- The threaded endpoint intentionally performs CPU-heavy work during the request.
- The queue endpoint is closer to a production pattern because the API process only enqueues work.
- For a no-GIL comparison, run the same benchmark with a regular Python build and a free-threaded Python build, then compare the reported durations.
