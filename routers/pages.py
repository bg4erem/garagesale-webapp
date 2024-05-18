from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from settings import settings
from uuid import uuid4

router = APIRouter()

templates = Jinja2Templates("page_templates")

@router.get("/favicon.ico", include_in_schema=False)
async def return_favicon():
    return FileResponse("favicon.ico")

@router.get("/page_templates/{file_path:path}", include_in_schema=False)
async def return_page_files(file_path: str):
    filepath = f"page_templates/{file_path}"
    return FileResponse(filepath)

@router.get("/")
async def render_home(r: Request):
    response = FileResponse("page_templates/home/index.html")

    client_id_cookie = r.cookies.get("X-Client-ID")
    if not client_id_cookie:
        response.set_cookie("X-Client-ID", uuid4().hex)
    
    return response

@router.get("/details/{item_id}")
async def render_details_page(r: Request, item_id: str):
    context = {
        "TELEGRAM_USERNAME": settings.TELEGRAM_USERNAME,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER
    }
    response = templates.TemplateResponse(r, "item_details/index.html", context)
    client_id_cookie = r.cookies.get("X-Client-ID")
    if not client_id_cookie:
        response.set_cookie("X-Client-ID", uuid4().hex)

    return response

@router.get("/admin_page")
async def render_admin_page():
    return FileResponse("page_templates/admin.html")