from enum import Enum
from pydantic import BaseModel

class Realtor_Reviews(BaseModel):
    user_id: int
    realtor_user_id: int
    rating: float
    review: str

class Vendor_Reviews(BaseModel):
    user_id: int
    vendor_user_id: int
    rating: float
    review: str
    