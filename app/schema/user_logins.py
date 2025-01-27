from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class User_Logins(BaseModel):
    user_id: str
    email_login: bool
    email: Optional[str]
    phone_login: bool
    phone: Optional[str]
    gmail_login: bool
    gmail: Optional[str]
