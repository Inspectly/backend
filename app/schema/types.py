from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class User_Type(str, Enum):
    ADMIN = 'admin'
    CLIENT = 'client'
    REALTOR = 'realtor'
    VENDOR = 'vendor'

class User_Types(BaseModel):
    user_type: User_Type

class Vendor_Type(str, Enum):
    GENERAL = 'general'
    STRUCTURAL = 'structural'
    ELECTRICIAN = 'electrician'
    PLUMBER = 'plumber'
    PAINTER = 'painter'
    CLEANER = 'cleaner'
    HVAC = 'hvac'
    ROOFING = 'roofing'
    INSULATION = 'insulation'
    DRYWALL = 'drywall'
    PLASTER = 'plaster'
    CARPENTRY = 'carpentry'
    LANDSCAPING = 'landscaping'
    OTHER = 'other'

class Vendor_Types(BaseModel):
    vendor_type: Vendor_Type

class Login_Method(str, Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    GMAIL = 'gmail'

class Status(str, Enum):
    OPEN = 'open'
    REVIEW = 'review'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed' 
