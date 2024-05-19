import aiohttp
from database import ips_collection

async def lookup_ip(ip: str) -> dict | None:
    ip_stored: dict | None = await ips_collection.find_one({"ip":ip}, {"_id":0})

    if not ip_stored:
        async with aiohttp.ClientSession() as session:
            print(f"calling api to look up ip {ip}")
            async with session.get(f"https://ipapi.co/{ip}/json/") as response:
                print(await response.text())
                ip_info = await response.json()
        if type(ip_info) is dict and ip_info.get("ip"):
            ip_info["_id"] = ip
            await ips_collection.insert_one(ip_info)
        else:
            ip_info = None
    else:
        ip_info = ip_stored

    return ip_info