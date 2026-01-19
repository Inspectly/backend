from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any

from app.schema.types import Login, User_Types, Vendor_Types

class Users(BaseModel):
    user_type: User_Types
    firebase_id: str

class Clients(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class Realtors(BaseModel):
    realtor_user_id: int
    realtor_firm_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    rating: Optional[int] = Field(default = -1)
    review: Optional[str] = None

    @validator('rating')
    def set_default_rating(cls, v):
        return v if v is not None else -1

class Vendors(BaseModel):
    vendor_user_id: int
    vendor_type: Vendor_Types
    vendor_types: str
    code: str
    license: Optional[str] = None
    verified: bool = Field(default = False)
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    rating: Optional[int] = Field(default = -1)
    review: Optional[str] = None
    years_of_experience: Optional[int] = None
    service_area: Optional[str] = None
    response_time: Optional[str] = None
    insurance: Optional[str] = None
    warranty: Optional[str] = None

    @validator('rating')
    def set_default_rating(cls, v):
        return v if v is not None else -1

class User_Logins(BaseModel):
    user_id: int
    email_login: bool = Field(default = False)
    email: Optional[str] = None
    phone_login: bool = Field(default = False)
    phone: Optional[str] = None
    gmail_login: bool = Field(default = False)
    gmail: Optional[str] = None

class User_Sessions(BaseModel):
    user_id: int
    login: Login
    login_time: str
    logout_time: Optional[str] = None
    authentication_code: str
