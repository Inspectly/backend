from fastapi import APIRouter, HTTPException

from app.crud import report_assessment_comments
from app.schema.properties import Report_Assessment_Comments

router = APIRouter()

@router.get('/')
def get_all():
    return report_assessment_comments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return report_assessment_comments.get_one(id)

@router.get('/report_assessment/{report_assessment_id}')
def get_all_by_report_assessment_id(report_assessment_id: int):
    return report_assessment_comments.get_all_by_report_assessment_id(report_assessment_id)

@router.get('/user/{user_id}')
def get_all_by_user_id(user_id: int):
    return report_assessment_comments.get_all_by_user_id(user_id)

@router.get('/user/{user_id}/report_assessment/{report_assessment_id}')
def get_comments_by_user_id_and_report_assessment_id(user_id: int, report_assessment_id: int):
    return report_assessment_comments.get_comments_by_user_id_and_report_assessment_id(user_id, report_assessment_id)

@router.post('/')
def create(report_assessment_comment: Report_Assessment_Comments):
    return report_assessment_comments.create(report_assessment_comment)

@router.put('/{id}')
def update(id: int, report_assessment_comment: Report_Assessment_Comments):
    return report_assessment_comments.update(id, report_assessment_comment)

@router.delete('/{id}/report_assessment/{report_assessment_id}')
def delete(id: int, report_assessment_id: int):
    return report_assessment_comments.delete(id, report_assessment_id)
