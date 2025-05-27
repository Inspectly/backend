from fastapi import APIRouter, HTTPException, Body

from app.crud import issues
from app.schema.properties import Issues

router = APIRouter()

@router.get('/')
def get_all():
    return issues.get_all()

@router.get('/total')
def total_issues_count():
    return issues.total_issues_count()

@router.get('/filter/total')
def total_issues_count_paginated(type = None, city = None, state = None, search = None):
    return issues.total_issues_count_filtered(type, city, state, search)

@router.get('/paginate')
def get_all_limit_offset(limit: int = 100, offset: int = 0, type = None, city = None, state = None, search = None):
    return issues.get_all_paginated(limit, offset, type, city, state, search)

@router.get('/{id}')
def get_one(id: int):
    return issues.get_one(id)

@router.get('/report/{report_id}')
def get_report_issues(report_id: int):
    return issues.get_report_issues(report_id)

@router.get('/vendor/{vendor_id}')
def get_vendor_issues(vendor_id: int):
    return issues.get_vendor_issues(vendor_id)

@router.get('/addresses/all')
def get_all_issue_addresses():
    return issues.get_all_issue_addresses()

@router.post('/addresses/issue_ids')
def get_all_issue_addresses_issue_ids(issue_ids: list[int] = Body(..., embed = True)):
    return issues.get_all_issue_addresses_issue_ids(issue_ids)

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
