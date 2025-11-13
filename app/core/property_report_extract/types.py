from typing import List
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class IssueTypes(str, Enum):
    roofing = 'ROOFING'
    exterior = 'EXTERIOR'
    structure = 'STRUCTURE'
    electrical = 'ELECTRICAL'
    heating = 'HEATING'
    cooling = 'COOLING'
    insulation = 'INSULATION'
    plumbing = 'PLUMBING'
    interior = 'INTERIOR'
    other = 'OTHER'

class Issue(BaseModel):
    id: int = Field(..., description = 'The id of the issue')
    name: str = Field(..., description = 'The name/title of the issue, typically extracted from issue headings. Often formatted as "CATEGORY \ Subcategory" (e.g., "SLOPED ROOF FLASHINGS \ Roof/sidewall flashings"). This is the title that appears at the start of each issue block.')
    description: str = Field(..., description = 'A multiline string containing the complete issue details including: Condition (current state/problem), Implication(s) (potential consequences), Location (where in the property), and Task (recommended action: Improve/Repair/Monitor/etc). Preserve the original formatting with labels like "Condition:", "Implication(s):", "Location:", "Task:".')
    images: List[str] = Field(default_factory = list, description = 'List of image filenames referenced in the markdown for this issue (e.g., ["ME_page_2_image_1.png", "ME_page_3_image_1.jpeg"]). Extract from image references like ![ref](filename).')
    type: Optional[IssueTypes] = Field(default = None, description = 'The system or category name from the inspection report. Must match one of: ROOFING, EXTERIOR, STRUCTURE, ELECTRICAL, HEATING, COOLING, INSULATION, PLUMBING, INTERIOR, or other if not in this list. Extract from section headers.')
    
class ReportIssues(BaseModel):
    issues: List[Issue] = Field(..., description = 'Complete list of all issue categories/systems found in the inspection report. Each entry represents a major system (ROOFING, ELECTRICAL, etc.) with its description and all associated issues. Exclude SUMMARY, SITE INFO, and REFERENCE sections as these are not issue categories.')

class ImageClassification(BaseModel):
    is_issue: bool = Field(..., description = 'Whether the image shows an issue (ROOFING, EXTERIOR, STRUCTURE, ELECTRICAL, HEATING, COOLING, INSULATION, PLUMBING, INTERIOR or other) related to a problem with a house or not.')
    reason: str = Field(..., description = 'a couple sentences explaining the reason for the classification. Must be one of the following: ROOFING, EXTERIOR, STRUCTURE, ELECTRICAL, HEATING, COOLING, INSULATION, PLUMBING, INTERIOR or other.')
