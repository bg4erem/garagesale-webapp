from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from models.stats import request_log
from routers.pages import router as router_pages
from routers.api import router as router_api
from fastapi.middleware.gzip import GZipMiddleware
import time
from database import requests_collection
from db_opensearch import INDEX_REQUESTS, client as opensearch_client

app = FastAPI(title="Garage Sale Webapp")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(router_api)
app.include_router(router_pages)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time

    print(f"{request.client.host}, {request.url.path}, {round(process_time, 3)}, {response.status_code}")

    log = await request_log(request, response, process_time)
    bg_tasks = BackgroundTasks()
    bg_tasks.add_task(requests_collection.insert_one, log)
    if opensearch_client:
        bg_tasks.add_task(opensearch_client.index(INDEX_REQUESTS, log))

    response.background = bg_tasks

    return response