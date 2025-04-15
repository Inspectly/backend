from fastapi import APIRouter, HTTPException

from app.crud import issue_assessment_comments
from app.schema.properties import Issue_Assessment_Comments

router = APIRouter()

@router.get('/')
def get_all():
    return issue_assessment_comments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return issue_assessment_comments.get_one(id)

@router.get('/issue_assessment/{issue_assessment_id}')
def get_all_by_issue_assessment_id(issue_assessment_id: int):
    return issue_assessment_comments.get_all_by_issue_assessment_id(issue_assessment_id)

@router.get('/user/{user_id}')
def get_all_by_user_id(user_id: int):
    return issue_assessment_comments.get_all_by_user_id(user_id)

@router.get('/user/{user_id}/issue_assessment/{issue_assessment_id}')
def get_comments_by_user_id_and_issue_assessment_id(user_id: int, issue_assessment_id: int):
    return issue_assessment_comments.get_comments_by_user_id_and_issue_assessment_id(user_id, issue_assessment_id)

@router.post('/')
def create(issue_assessment_comment: Issue_Assessment_Comments):
    return issue_assessment_comments.create(issue_assessment_comment)

@router.put('/{id}')
def update(id: int, issue_assessment_comment: Issue_Assessment_Comments):
    return issue_assessment_comments.update(id, issue_assessment_comment)

@router.delete('/{id}/issue_assessment/{issue_assessment_id}')
def delete(id: int, issue_assessment_id: int):
    return issue_assessment_comments.delete(id, issue_assessment_id)
