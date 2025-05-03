from fastapi import APIRouter, HTTPException

from app.crud import issue_assessments
from app.schema.properties import Issue_Assessments, Issue_Assessments_Delete

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

@router.get('/users_interaction/{users_interaction_id}')
def get_all_by_users_interaction_id(users_interaction_id: str):
    return issue_assessments.get_all_by_users_interaction_id(users_interaction_id)

@router.get('/user_id/{user_id}')
def get_all_by_user_id(user_id: int):
    return issue_assessments.get_all_by_user_id(user_id)

@router.get('/user_id_users_interaction_id/{user_id}')
def get_all_by_user_id_users_interaction_id(user_id: int):
    return issue_assessments.get_all_by_user_id_users_interaction_id(user_id)

@router.get('/vendor_id_users_interaction_id/{vendor_id}')
def get_all_by_vendor_id_users_interaction_id(vendor_id: int):
    return issue_assessments.get_all_by_vendor_id_users_interaction_id(vendor_id)

@router.post('/')
def create(issue_assessment: Issue_Assessments):
    return issue_assessments.create(issue_assessment)

@router.put('/{id}')
def update(id: int, issue_assessment: Issue_Assessments):
    return issue_assessments.update(id, issue_assessment)

@router.delete('/{id}')
def delete(id: int, params: Issue_Assessments_Delete):
    return issue_assessments.delete(id, params.issue_id, params.interaction_id)
