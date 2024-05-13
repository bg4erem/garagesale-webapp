import random
import string
from typing import override
from fastapi import UploadFile
from pydantic import BaseModel, Field


def random_uid():
    alphabet = string.ascii_lowercase + string.digits
    rand_sequense = ''.join(random.choices(alphabet, k=7))
    
    PREFIX = "item-"
    full_random_id = f"{PREFIX}{rand_sequense}".upper()
    
    return full_random_id


class ItemProperty(BaseModel):
    name: str
    value: str
    display: bool = True


class Item(BaseModel):
    id: str = Field(default_factory=random_uid, alias="_id")
    title: str
    description: str = ""
    full_price: float | None = None
    price: float
    price_curr: str = "KZT"
    photos: list[str] = []
    properties: list[ItemProperty] = []
    sold: bool = False