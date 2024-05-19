import motor.motor_asyncio
from models.stats import ItemView
from ip_lookup import lookup_ip

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.garage_sale_webapp

items_collection = db["items"]
views_collection = db["views"]
views_general_collection = db["views_general"]
ips_collection = db["ips"]

async def record_item_view(id: str, ip:str=None, useragent:str=None, client_id:str=None):
    ip_info = None
    if ip:
        ip_stored = await ips_collection.find_one({"ip":ip})
        if not ip_stored:
            ip_info = await lookup_ip(ip)
            if ip_info:
                ip_info["_id"] = ip
                await ips_collection.insert_one(ip_info)
        else:
            ip_info = ip_stored

    view = ItemView(item_id=id, ip=ip, useragent=useragent, client_id=client_id)
    view.ip_lookup = ip_info
    await views_collection.insert_one(view.model_dump())

    views = await views_collection.count_documents({"item_id": id})

    await views_general_collection.update_one({"_id": id}, {"$set": {"all": views}}, upsert=True)