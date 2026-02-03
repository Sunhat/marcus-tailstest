from pydantic import BaseModel, field_validator, Field
from typing import Optional, Literal
from enum import Enum

class OrderDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class StoresListQuery(BaseModel):
    order: Optional[OrderDirection] = None
    @field_validator("order", mode="before")
    @classmethod
    def validate_order(cls, value: Optional[str]) -> Optional[OrderDirection]:
        if value is None:
            return None
        try:
            return OrderDirection(value)
        except ValueError:
            return None

class StoresNearbyQuery(BaseModel):
    postcode: str
    radius_km: float

class Store(BaseModel):
    name: str
    postcode: str
    latitude: float
    longitude: float

