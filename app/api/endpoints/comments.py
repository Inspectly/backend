from fastapi import APIRouter, HTTPException

from app.crud import comments
from app.schema.properties import Comments

router = APIRouter()

@router.get('/')
def get_all():
    return comments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return comments.get_one(id)

@router.get('/issue/{issue_id}')
def get_issue_comments(issue_id: int):
    return comments.get_issue_comments(issue_id)

@router.get('/user/{user_id}')
def get_user_comments(user_id: int):
    return comments.get_user_comments(user_id)

@router.post('/')
def create(comment: Comments):
    return comments.create(comment)

@router.put('/{id}')
def update(id: int, comment: Comments):
    return comments.update(id, comment)

@router.delete('/{id}')
def delete(id: int):
    return comments.delete(id)
