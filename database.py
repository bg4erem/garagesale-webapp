from fastapi import Request
import motor.motor_asyncio
from models.stats import ItemView
from db_opensearch import client as opensearch_client, INDEX_ITEMS_VIEWS, INDEX_REQUESTS

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.garage_sale_webapp

items_collection = db["items"]
views_collection = db["views"]
views_general_collection = db["views_general"]
ips_collection = db["ips"]
requests_collection = db["requests"]

async def record_item_view(id: str, r: Request):
    from ip_lookup import lookup_ip

    ip:str= r.client.host
    useragent:str= r.headers.get("user-agent")
    client_id:str= r.cookies.get("X-Client-ID")

    view = ItemView(item_id=id, ip=ip, useragent=useragent, client_id=client_id)
    view.ip_lookup = await lookup_ip(ip)
    await views_collection.insert_one(view.model_dump())
    if opensearch_client:
        view.item = await items_collection.find_one({"_id": id})
        await opensearch_client.index(INDEX_ITEMS_VIEWS, view.model_dump())

    views = await views_collection.count_documents({"item_id": id})

    await views_general_collection.update_one({"_id": id}, {"$set": {"all": views}}, upsert=True)