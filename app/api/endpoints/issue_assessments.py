from fastapi import APIRouter, HTTPException

from app.crud import issue_assessments
from app.schema.properties import Issue_Assessments

router = APIRouter()

@router.get('/')
def get_all():
    return issue_assessments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return issue_assessments.get_one(id)

@router.get('/issue/{issue_id}')
def get_all_by_issue_id(issue_id: int):
    return issue_assessments.get_all_by_issue_id(issue_id)

@router.get('/vendor/{vendor_id}/issue/{issue_id}')
def get_all_by_vendor_id(vendor_id: int, issue_id: int):
    return issue_assessments.get_all_by_vendor_id(vendor_id, issue_id)

@router.post('/')
def create(issue_assessment: Issue_Assessments):
    return issue_assessments.create(issue_assessment)

@router.put('/{id}')
def update(id: int, issue_assessment: Issue_Assessments):
    return issue_assessments.update(id, issue_assessment)

@router.delete('/{id}')
def delete(id: int):
    return issue_assessments.delete(id)
