import motor.motor_asyncio
from models.stats import ItemView

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.garage_sale_webapp

items_collection = db["items"]
views_collection = db["views"]
views_general_collection = db["views_general"]

async def record_item_view(id: str, ip:str=None, useragent:str=None, client_id:str=None):
    view = ItemView(item_id=id, ip=ip, useragent=useragent, client_id=client_id)
    await views_collection.insert_one(view.model_dump())

    views = await views_collection.count_documents({"item_id": id})

    await views_general_collection.update_one({"_id": id}, {"$set": {"all": views}}, upsert=True)