from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Reports(BaseModel):
    user_id: str
    aws_link: str
    name: str
    city: str
    state: str
    country: str
    postal_code: str
