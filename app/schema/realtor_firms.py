from pydantic import BaseModel
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
    rating: Optional[int]
    review: Optional[str]
