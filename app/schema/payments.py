from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Payments(BaseModel):
    user_id: str
    payment_amount: float
