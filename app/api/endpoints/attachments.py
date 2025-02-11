from fastapi import APIRouter, HTTPException

from app.crud import attachments
from app.schema.properties import Attachments

router = APIRouter()

@router.get('/')
def get_all():
    return attachments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return attachments.get_one(id)

@router.get('/issue/{issue_id}')
def get_issue_attachments(issue_id: int):
    return attachments.get_issue_attachments(issue_id)

@router.get('/user/{user_id}')
def get_user_attachments(user_id: int):
    return attachments.get_user_attachments(user_id)

@router.post('/')
def create(attachment: Attachments):
    return attachments.create(attachment)

@router.put('/{id}')
def update(id: int, attachment: Attachments):
    return attachments.update(id, attachment)

@router.delete('/{id}')
def delete(id: int):
    return attachments.delete(id)
