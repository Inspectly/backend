from fastapi import APIRouter, HTTPException

from app.crud import notes
from app.schema.properties import Notes

router = APIRouter()

@router.get('/')
def get_all():
    return notes.get_all()

@router.get('/{id}')
def get_one(id: int):
    return notes.get_one(id)

@router.get('/report/{report_id}')
def get_report_notes(report_id: int):
    return notes.get_report_notes(report_id)

@router.get('/user/{user_id}')
def get_user_notes(user_id: int):
    return notes.get_user_notes(user_id)

@router.post('/')
def create(note: Notes):
    return notes.create(note)

@router.put('/{id}')
def update(id: int, note: Notes):
    return notes.update(id, note)

@router.delete('/{id}')
def delete(id: int):
    return notes.delete(id)
