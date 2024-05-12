import os
from datetime import datetime, timedelta, timezone
import aiofiles
from fastapi import APIRouter, Cookie, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from models.items import Item
from database import items_collection
from settings import settings
from PIL import Image

router = APIRouter(prefix="/api/v1")

ADMIN_PIN = settings.ADMIN_PIN

@router.post("/verify_pin")
async def authenticate_admin_pin(pin: str):
    if pin == ADMIN_PIN:
        expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)
        response = JSONResponse(status_code=200, content={"message": "Authentication successful"})
        response.set_cookie(key="adminPin", value=pin, expires=expiration_time, path="/")
        return response
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

@router.post("/upload_files")
async def upload_files(files: list[UploadFile]):
    filepathes = []

    for file in files:
        filename = file.filename
        save_path = f"media/{filename}"
        async with aiofiles.open(save_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        compressed_path = f"{save_path}.webp"
        image = Image.open(save_path)
        image = image.convert("RGB")
        image.save(compressed_path, 'webp', optimize=True, quality=85)
        
        os.remove(save_path)
        filepathes.append(f"/{compressed_path}")
    
    return filepathes

@router.get("/items")
async def return_items(id: str|None = None):
    if id:
        item = await items_collection.find_one({"_id":id})
        return Item(**item)
    else:
        items = await items_collection.find({}).to_list(10_000)
        items = [Item(**item) for item in items]
        return items

@router.post("/items")
async def create_item(item: Item, admin_pin: str = Cookie(None, alias="adminPin")):
    if admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        await items_collection.insert_one(item.model_dump(by_alias=True))
        return True
    except Exception as e:
        print(e)
        return JSONResponse({"error":e}, status.HTTP_500_INTERNAL_SERVER_ERROR)