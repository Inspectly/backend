from pydantic import BaseModel
from typing import Optional, Dict, Any

class Checkout_Session_Request(BaseModel):
    client_id: int
    vendor_id: int
    offer_id: int

class Checkout_Session_Response(BaseModel):
    session_id: str
    url: str

