from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class User_Type(str, Enum):
    ADMIN = 'admin'
    INDIVIDUAL = 'individual'
    BROKER = 'broker'
    REALTOR = 'realtor'
    CONTRACTOR = 'contractor'

class User_Types(BaseModel):
    user_type: User_Type
