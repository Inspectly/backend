from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.schema.types import Status

class Listings(BaseModel):
    user_id: int
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    image_url: Optional[str]

class Reports(BaseModel):
    user_id: int
    listing_id: int
    aws_link: str
    name: str
    
class Issues(BaseModel):
    report_id: int
    vendor_id: int
    type: str
    description: Optional[str]
    summary: Optional[str]
    severity: Optional[str]
    status: Status
    active: bool
    cost: Optional[float]
    image_url: Optional[str]

class Attachments(BaseModel):
    issue_id: int
    user_id: int
    name: str
    type: str
    url: str

class Comments(BaseModel):
    issue_id: int
    user_id: int
    comment: str

class Notes(BaseModel):
    report_id: int
    user_id: int
    note: str
