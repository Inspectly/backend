from pydantic import BaseModel

class Issue(BaseModel):
    name: str
    description: str
    # images: list[str]

class Issue_Type(BaseModel):
    type: str
    descriptions: str
    issues: list[Issue]

class Report_Response(BaseModel):
    IssueTypes: list[Issue_Type]
