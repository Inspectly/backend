from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Payments(BaseModel):
    user_id: str
    payment_amount: float
    expiry_date: str
    stripe_payment_id: str
    stripe_user_id: str
