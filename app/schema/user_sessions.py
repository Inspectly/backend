from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Login_Method(str, Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    GMAIL = 'gmail'

class User_Sessions(BaseModel):
    user_id: str
    login_method: Login_Method
    authentication_code: str
