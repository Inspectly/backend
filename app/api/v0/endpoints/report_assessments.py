from fastapi import APIRouter, HTTPException

from app.crud import report_assessments
from app.schema.properties import Report_Assessments, Report_Assessments_Delete

router = APIRouter()

@router.get('/')
def get_all():
    return report_assessments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return report_assessments.get_one(id)

@router.get('/report/{report_id}')
def get_all_by_report_id(report_id: int):
    return report_assessments.get_all_by_report_id(report_id)

@router.get('/users_interaction/{users_interaction_id}')
def get_all_by_users_interaction_id(users_interaction_id: str):
    return report_assessments.get_all_by_users_interaction_id(users_interaction_id)

@router.get('/user_id/{user_id}')
def get_all_by_user_id(user_id: int):
    return report_assessments.get_all_by_user_id(user_id)

@router.get('/client_id_users_interaction_id/{client_id}')
def get_all_by_client_id_users_interaction_id(client_id: int):
    return report_assessments.get_all_by_client_id_users_interaction_id(client_id)

@router.get('/vendor_id_users_interaction_id/{vendor_id}')
def get_all_by_vendor_id_users_interaction_id(vendor_id: int):
    return report_assessments.get_all_by_vendor_id_users_interaction_id(vendor_id)

@router.post('/')
def create(report_assessment: Report_Assessments):
    return report_assessments.create(report_assessment)

@router.put('/{id}')
def update(id: int, report_assessment: Report_Assessments):
    return report_assessments.update(id, report_assessment)

@router.delete('/{id}')
def delete(id: int, params: Report_Assessments_Delete):
    return report_assessments.delete(id, params.report_id, params.interaction_id)
