from typing import TypedDict
from datetime import datetime, timezone
from fastapi import Request, Response
from pydantic import BaseModel, Field

def get_now_utc() -> datetime:
    return datetime.now(timezone.utc)

class ItemView(BaseModel, extra="allow"):
    timestamp: datetime = Field(default_factory=get_now_utc)
    item_id: str
    ip: str = None
    useragent: str = None
    client_id: str = None
    ip_lookup: dict | None = None

async def request_log(request: Request, response: Response, process_time: float):
    from ip_lookup import lookup_ip
    class RequestLog(TypedDict):
        timestamp: datetime
        ip: str
        request_uri: str
        method: str
        process_time: float
        status_code: int
        user_agent: str|None
        ip_lookup: dict
        location: list[float]|None

    ip_lookup = await lookup_ip(request.client.host)
    location = None
    if ip_lookup.get("longitude") and ip_lookup.get("latitude"):
        location = [ip_lookup.get("longitude"), ip_lookup.get("latitude")]

    request_log: RequestLog = {
        "timestamp": datetime.now(timezone.utc),
        "ip": request.client.host,
        "request_uri": request.url.path,
        "method": request.method,
        "process_time": process_time,
        "status_code": response.status_code,
        "ip_lookup": ip_lookup,
        "user_agent": request.headers.get("User-Agent"),
        "location": location
    }

    return request_log