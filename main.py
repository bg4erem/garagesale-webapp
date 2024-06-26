from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from models.stats import request_log
from routers.pages import router as router_pages
from routers.api import router as router_api
from fastapi.middleware.gzip import GZipMiddleware
import time
from database import requests_collection
from db_opensearch import INDEX_REQUESTS, client as opensearch_client
from limiter import limiter_per_address, RateLimitExceeded, _rate_limit_exceeded_handler

app = FastAPI(title="Garage Sale Webapp", docs_url=None, redoc_url=None)
app.state.limiter = limiter_per_address
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(router_api)
app.include_router(router_pages)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time

    log = await request_log(request, response, process_time)
    async def log_request(log):
        if opensearch_client:
            await opensearch_client.index(INDEX_REQUESTS, log)
        await requests_collection.insert_one(log)
        
    bg_tasks = BackgroundTasks()
    bg_tasks.add_task(log_request, log)

    response.background = bg_tasks

    return response