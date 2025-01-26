from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.schema.user_types import User_Types

class Users(BaseModel):
    user_type: User_Types
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    user_code: int
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
