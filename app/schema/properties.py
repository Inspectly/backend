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

class Reports_Simple(BaseModel):
    user_id: int
    listing_id: int
    name: str

class Reports(BaseModel):
    user_id: int
    listing_id: int
    aws_link: Optional[str] = None
    name: str

class Report_Offers(BaseModel):
    report_id: int
    vendor_id: Optional[int] = None
    price: float
    status: Bid_Status
    user_last_viewed: Optional[str] = None
    comment_vendor: Optional[str] = None
    comment_client: Optional[str] = None

class Report_Assessments(BaseModel):
    report_id: int
    user_id: int
    user_type: User_Type
    interaction_id: str
    users_interaction_id: str
    start_time: str
    end_time: str
    status: Assessment_Status
    user_last_viewed: Optional[str] = None
    min_assessment_time: Optional[int] = None

class Report_Assessments_Delete(BaseModel):
    report_id: int
    interaction_id: str

class Report_Assessment_Comments(BaseModel):
    report_assessment_id: int
    user_id: int
    comment: str
    
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
    vendor_id: Optional[int] = None
    price: float
    status: Bid_Status
    user_last_viewed: Optional[str] = None
    comment_vendor: Optional[str] = None
    comment_client: Optional[str] = None

class Issue_Assessments(BaseModel):
    issue_id: int
    user_id: int
    user_type: User_Type
    interaction_id: str
    users_interaction_id: str
    start_time: str
    end_time: str
    status: Assessment_Status
    user_last_viewed: Optional[str] = None
    min_assessment_time: Optional[int] = None

class Issue_Assessments_Delete(BaseModel):
    issue_id: int
    interaction_id: str

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
