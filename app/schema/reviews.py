from pydantic import BaseModel
from app.schema.types import Review_Status

class Client_Reviews(BaseModel):
    user_id: int
    client_user_id: int
    status: Review_Status = Review_Status.PENDING
    rating: float
    review: str

class Realtor_Reviews(BaseModel):
    user_id: int
    realtor_user_id: int
    status: Review_Status = Review_Status.PENDING
    rating: float
    review: str

class Vendor_Reviews(BaseModel):
    user_id: int
    vendor_user_id: int
    status: Review_Status = Review_Status.PENDING
    rating: float
    review: str
