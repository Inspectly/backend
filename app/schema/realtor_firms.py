from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any

class Realtor_Firms(BaseModel):
    name: str
    code: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    rating: Optional[int] = Field(default = -1)
    review: Optional[str] = None

    @validator('rating')
    def set_default_rating(cls, v):
        return v if v is not None else -1
