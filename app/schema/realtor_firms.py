from pydantic import BaseModel, Field
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
    review: Optional[str]
