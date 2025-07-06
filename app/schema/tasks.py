from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'

class Task_Type(str, Enum):
    EXTRACT_ISSUES = 'extract_issues'
    EXTRACT_IMAGES = 'extract_images'

class Tasks(BaseModel):
    report_id: int
    task_type: Task_Type
    status: Status
