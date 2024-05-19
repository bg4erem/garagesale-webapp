import aiohttp

async def lookup_ip(ip: str):
    async with aiohttp.ClientSession() as session:
        print(f"calling api to look up ip {ip}")
        async with session.get(f"https://ipapi.co/{ip}/json/") as response:
            print(await response.text())
            ip_info = await response.json()
        
    if not type(ip_info) is dict:
        ip_info = None

    return ip_info