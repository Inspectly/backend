from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.schema.types import Assessment_Status, Bid_Status, Status

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
    type: str
    vendor_id: Optional[int]
    description: Optional[str]
    summary: Optional[str]
    severity: Optional[str]
    status: Status
    active: bool
    image_url: Optional[str]

class Issue_Offers(BaseModel):
    issue_id: int
    vendor_id: Optional[int]
    price: float
    status: Bid_Status
    comment_vendor: Optional[str]
    comment_client: Optional[str]

class Issue_Assessments(BaseModel):
    issue_id: int
    vendor_id: int
    date: str
    status: Assessment_Status
    comment_vendor: Optional[str]
    comment_client: Optional[str]

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
