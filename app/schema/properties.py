from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.schema.types import Progress_Steps

class Listings(BaseModel):
    user_id: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    image_url: Optional[str]

class Reports(BaseModel):
    user_id: str
    listing_id: str
    aws_link: str
    name: str
    
class Issues(BaseModel):
    report_id: str
    vendor_id: str
    type: str
    description: Optional[str]
    summary: Optional[str]
    severity: Optional[str]
    progress: Progress_Steps
    active: bool
    cost: Optional[float]

class Attachments(BaseModel):
    issue_id: str
    user_id: str
    name: str
    attachment_type: str
    url: str

class Comments(BaseModel):
    issue_id: str
    user_id: str
    comment: str

class Notes(BaseModel):
    report_id: str
    user_id: str
    note: str
