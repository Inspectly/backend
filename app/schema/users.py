from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from user_types import User_Types

class Users(BaseModel):
    user_type: User_Types
    name: str
    email: str
    phone: str
    address: str
    user_code: int
    city: str
    state: str
    country: str
    postal_code: str
