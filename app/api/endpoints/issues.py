from fastapi import APIRouter, HTTPException

from app.crud import issues
from app.schema.properties import Issues

router = APIRouter()

@router.get('/')
def get_all():
    return issues.get_all()

@router.get('/{id}')
def get_one(id: int):
    return issues.get_one(id)

@router.get('/report/{report_id}')
def get_report_issues(report_id: int):
    return issues.get_report_issues(report_id)

@router.get('/vendor/{vendor_id}')
def get_vendor_issues(vendor_id: int):
    return issues.get_vendor_issues(vendor_id)

@router.get('/address/{id}')
def get_issue_address(id: int):
    return issues.get_issue_address(id)

@router.post('/')
def create(issue: Issues):
    return issues.create(issue)

@router.put('/{id}')
def update(id: int, issue: Issues):
    return issues.update(id, issue)

@router.delete('/{id}')
def delete(id: int):
    return issues.delete(id)
