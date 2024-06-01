import hashlib
import os
from datetime import datetime, timedelta, timezone
import random
import aiofiles
from fastapi import APIRouter, BackgroundTasks, Cookie, HTTPException, Request, UploadFile, status
from fastapi.responses import JSONResponse
from models.items import Item
from database import items_collection, views_general_collection, record_item_view
from settings import settings
from PIL import Image, ImageOps
from limiter import limiter_per_address

router = APIRouter(prefix="/api/v1")

ADMIN_PIN = settings.ADMIN_PIN

@router.post("/verify_pin")
@limiter_per_address.limit("5/minute")
async def authenticate_admin_pin(request: Request, pin: str):
    if pin == ADMIN_PIN:
        expiration_time = datetime.now(timezone.utc) + timedelta(hours=24)
        response = JSONResponse(status_code=200, content={"message": "Authentication successful"})
        response.set_cookie(key="adminPin", value=pin, expires=expiration_time, path="/")
        return response
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")

@router.post("/upload_files")
async def upload_files(files: list[UploadFile], admin_pin: str = Cookie(None, alias="adminPin")):
    if admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    filepathes = []

    for file in files:
        filename = file.filename
        save_path = f"media/{filename}"
        async with aiofiles.open(save_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        if file.content_type.startswith("image/"):
            compressed_path = f"{save_path}.jpeg"
            image = Image.open(save_path)
            image = image.convert("RGB")
            image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            image = ImageOps.exif_transpose(image)
            image.save(compressed_path, 'webp', optimize=True, quality=90)
            
            os.remove(save_path)
            filepathes.append(f"/{compressed_path}")
        else:
            filepathes.append(f"/{save_path}")
    
    return filepathes

@router.get("/items")
async def return_items(r: Request, bg_tasks: BackgroundTasks, id: str|None = None, record_view: bool = True):
    admin_cookie = r.cookies.get("adminPin")

    if id:
        item = await items_collection.find_one({"_id":id})
        item = Item(**item)
        item.views_all = await views_general_collection.find_one({"_id": id})
        item.views_all = item.views_all.get("all") if item.views_all else 1
        
        if record_view and not admin_cookie:
            bg_tasks.add_task(record_item_view, id, r)
        
        return item
    else:
        items = await items_collection.find({}).to_list(10_000)
        items = [Item(**item) for item in items]
        
        if r.cookies.get("X-Client-ID") and not admin_cookie:
            seed = int(hashlib.md5(r.cookies.get("X-Client-ID").encode()).hexdigest(), 16)
            random.seed(seed)
            random.shuffle(items)

        return items

@router.post("/items")
async def create_or_edit_item(item: Item, admin_pin: str = Cookie(None, alias="adminPin")):
    if admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        insertion_result = await items_collection.update_one({"_id": item.id}, {"$set": item.model_dump(by_alias=True)}, upsert=True)
        return insertion_result.upserted_id
    except Exception as e:
        print(e)
        return JSONResponse({"error":e}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/items/sold")
async def mark_item_sold(item_id: str, sold:bool=True, admin_pin: str = Cookie(None, alias="adminPin")):
    if admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    saved_item = await items_collection.find_one({"_id": item_id})
    if not saved_item:
        raise HTTPException(status_code=404, detail=f"Not found {item_id}")
    
    saved_item = Item(**saved_item)
    if sold:
        saved_item.sold = True
    else:
        saved_item.sold = False

    try:
        await items_collection.update_one({"_id":item_id}, {"$set":saved_item.model_dump(by_alias=True)})
        return True
    except Exception as e:
        print(e)
        return JSONResponse({"error":e}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/items")
async def edit_item(item: Item, item_id: str, admin_pin: str = Cookie(None, alias="adminPin")):
    if admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    saved_item = await items_collection.find_one({"_id": item_id})
    if not saved_item:
        raise HTTPException(status_code=404, detail=f"Not found {item_id}")
    
    try:
        await items_collection.update_one({"_id":item_id}, {"$set":item.model_dump(by_alias=True)})
        return True
    except Exception as e:
        print(e)
        return JSONResponse({"error":e}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.delete("/items")
async def edit_item(item_id: str, admin_pin: str = Cookie(None, alias="adminPin")):
    if admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    saved_item = await items_collection.find_one({"_id": item_id})
    if not saved_item:
        raise HTTPException(status_code=404, detail=f"Not found {item_id}")
    
    saved_item = Item(**saved_item)
    try:
        await items_collection.delete_one({"_id":item_id})
        all_items: list[Item] = await return_items()
        referenced_media_files = [media for item in all_items for media in item]
        for photo in saved_item.photos:
            if photo not in referenced_media_files: 
                os.remove(photo[1:])
                print(f"removed from disk: {photo}")
        return True
    except Exception as e:
        print(e)
        return JSONResponse({"error":e}, status.HTTP_500_INTERNAL_SERVER_ERROR)