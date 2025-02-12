from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Payments(BaseModel):
    user_id: int
    payment_amount: float
    expiry_date: str
    stripe_payment_id: str
    stripe_user_id: str

class User_Stripe_Information(BaseModel):
    user_id: int
    stripe_user_id: str
    