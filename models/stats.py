from typing import TypedDict
from datetime import datetime, timezone
from fastapi import Request, Response
from pydantic import BaseModel, Field
import user_agents

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
        user_agent_parse: dict|None
        cookies: dict|None

    ip_lookup = await lookup_ip(request.client.host)
    user_agent = request.headers.get("User-Agent")

    user_agent_parse = None
    if user_agent:
        user_agent_parse = {}
        try:
            user_agent_parse["is_bot"] = user_agents.parse(user_agent).is_bot
            user_agent_parse["is_email_client"] = user_agents.parse(user_agent).is_email_client
            user_agent_parse["is_mobile"] = user_agents.parse(user_agent).is_mobile
            user_agent_parse["is_pc"] = user_agents.parse(user_agent).is_pc
            user_agent_parse["is_tablet"] = user_agents.parse(user_agent).is_tablet
            user_agent_parse["base_string"] = str(user_agents.parse(user_agent))
            user_agent_parse["os_family"] = user_agents.parse(user_agent).os.family
            user_agent_parse["os_version_string"] = user_agents.parse(user_agent).os.version_string
            user_agent_parse["browser_family"] = user_agents.parse(user_agent).browser.family
            user_agent_parse["browser_version_string"] = user_agents.parse(user_agent).browser.version_string
            user_agent_parse["device_family"] = user_agents.parse(user_agent).device.family
            user_agent_parse["device_brand"] = user_agents.parse(user_agent).device.brand
            user_agent_parse["device_model"] = user_agents.parse(user_agent).device.model
        except:
            ...

    request_log: RequestLog = {
        "timestamp": datetime.now(timezone.utc),
        "ip": request.client.host,
        "request_uri": request.url.path,
        "method": request.method,
        "process_time": process_time,
        "status_code": response.status_code,
        "ip_lookup": ip_lookup,
        "user_agent": user_agent,
        "user_agent_parse": user_agent_parse,
        "cookies":request.cookies,
    }

    return request_log