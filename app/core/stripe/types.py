from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, Any

class Checkout_Session_Request(BaseModel):
    client_id: int
    vendor_id: int
    offer_id: int

class Checkout_Session_Response(BaseModel):
    session_id: str
    url: str

class Stripe_Checkout_Session(Enum):
    COMPLETED = 'checkout.session.completed'
    PAYMENT_SUCCEEDED = 'checkout.session.async_payment_succeeded'
    PAYMENT_FAILED = 'checkout.session.async_payment_failed'
    EXPIRED = 'checkout.session.expired'
