from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.schema.types import Assessment_Status, Bid_Status, Status, User_Type

class Listings(BaseModel):
    user_id: int
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    image_url: Optional[str] = None

class Reports(BaseModel):
    user_id: int
    listing_id: int
    aws_link: Optional[str] = None
    name: str
    
class Issues(BaseModel):
    report_id: int
    type: str
    vendor_id: Optional[int] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    severity: Optional[str] = None
    status: Status
    active: bool
    image_url: Optional[str] = None

class Issue_Offers(BaseModel):
    issue_id: int
    vendor_id: int
    price: float
    status: Bid_Status
    comment_vendor: Optional[str] = None
    comment_client: Optional[str] = None

class Issue_Assessments(BaseModel):
    issue_id: int
    user_id: int
    interaction_id: str
    user_type: User_Type
    start_time: str
    end_time: str
    status: Assessment_Status
    min_assessment_time: Optional[int] = None

class Issue_Assessment_Comments(BaseModel):
    issue_assessment_id: int
    user_id: int
    comment: str

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
