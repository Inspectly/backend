import os
import uuid
import logfire
from enum import Enum
from app.core.config import settings

from dotenv import load_dotenv
load_dotenv(override = True)

class Instrument_Type(Enum):
    PANDANTIC_AI = 'pydantic_ai'
    OPENAI = 'openai'

def instrument_logfire(instrument_type: Instrument_Type = Instrument_Type.PANDANTIC_AI, project: str = None, use_class_name: bool = False):
    def decorator(cls):
        original_init = cls.__init__
        
        def init_logfire(self, *args, **kwargs):
            if (use_class_name):
                prefix = cls.__name__.lower()
            else:
                prefix = project
            self.logfire = logfire.configure(
                token = settings.LOGFIRE_API_KEY,
                service_name = f'{prefix}-{str(uuid.uuid4())[:5]}' if prefix else str(uuid.uuid4())[:5],
                scrubbing = False,
                local = True
            )
            if (instrument_type == Instrument_Type.PANDANTIC_AI):
                self.logfire.instrument_pydantic_ai()
            elif (instrument_type == Instrument_Type.OPENAI):
                self.logfire.instrument_openai()
            
            original_init(self, *args, **kwargs)
        
        cls.__init__ = init_logfire
        return cls
    
    return decorator
