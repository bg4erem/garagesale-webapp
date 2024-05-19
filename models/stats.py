from datetime import datetime, timezone
from pydantic import BaseModel, Field

def get_now_utc() -> datetime:
    return datetime.now(timezone.utc)

class ItemView(BaseModel):
    timestamp: datetime = Field(default_factory=get_now_utc)
    item_id: str
    ip: str = None
    useragent: str = None
    client_id: str = None
    ip_lookup: dict | None = None