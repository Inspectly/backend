from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.schema.types import Login_Method, User_Types, Vendor_Types

class Users(BaseModel):
    user_type: User_Types

class Clients(BaseModel):
    realtor_user_id: str
    realtor_firm_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str

class Realtors(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    rating: Optional[int]
    review: Optional[str]

class Vendors(BaseModel):
    user_id: str
    vendor_type: Vendor_Types
    code: str
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    rating: Optional[int]
    review: Optional[str]

class User_Logins(BaseModel):
    user_id: str
    email_login: bool
    email: Optional[str]
    phone_login: bool
    phone: Optional[str]
    gmail_login: bool
    gmail: Optional[str]

class User_Sessions(BaseModel):
    user_id: str
    login_method: Login_Method
    authentication_code: str
