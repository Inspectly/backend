from fastapi import APIRouter, HTTPException

from app.crud import reports
from app.schema.reports import Reports

router = APIRouter()

@router.get('/')
def get_all():
    return reports.get_all()

@router.get('/{id}')
def get_one(id: int):
    return reports.get_one(id)

@router.get('/user/{user_id}')
def get_user_reports(user_id: int):
    return reports.get_user_reports(user_id)

@router.post('/')
def create(report: Reports):
    return reports.create(report)

@router.put('/{id}')
def update(id: int, report: Reports):
    return reports.update(id, report)

@router.delete('/{id}')
def delete(id: int):
    return reports.delete(id)
