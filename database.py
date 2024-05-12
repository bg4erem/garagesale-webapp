import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.garage_sale_webapp

items_collection = db["items"]