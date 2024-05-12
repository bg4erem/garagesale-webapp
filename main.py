from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.pages import router as router_pages
from routers.api import router as router_api
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(title="Garage Sale Webapp")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(router_api)
app.include_router(router_pages)