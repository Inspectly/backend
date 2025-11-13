from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Provider(str, Enum):
    openai = 'openai'
    anthropic = 'anthropic'
    google = 'google'

class ReasoningEffort(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class Settings(BaseModel):
    allow_temperature: Optional[bool]
    allow_reasoning_effort: Optional[bool]
    reasoning_effort: Optional[ReasoningEffort]

class Models(BaseModel):
    model_name: str
    provider: Provider
    model_settings: Optional[Settings]
