from fastapi import APIRouter, HTTPException, Request

from app.crud import users
from app.schema.users import Users

router = APIRouter()

@router.get('/')
def get_all():
    return users.get_all()

@router.get('/{id}')
def get_one(id: int):
    return users.get_one(id)

@router.get('/firebase/{firebase_id}')
def get_one_by_firebase_id(firebase_id: str):
    return users.get_one_by_firebase_id(firebase_id)

@router.post('/')
async def create(user: Users, request: Request):
    auth_user = getattr(request.state, 'user', None)
    if not auth_user or auth_user.get('firebase_id') != user.firebase_id:
        raise HTTPException(status_code = 403, detail = 'firebase_id must match the authenticated token')
    return await users.create(user)

@router.put('/{id}')
def update(id: int, user: Users, request: Request):
    auth_user = getattr(request.state, 'user', None)
    if not auth_user or auth_user.get('id') != id:
        raise HTTPException(status_code = 403, detail = 'Users can only update their own account')
    return users.update(id, user)

@router.delete('/{id}')
def delete(id: int, request: Request):
    auth_user = getattr(request.state, 'user', None)
    if not auth_user or auth_user.get('id') != id:
        raise HTTPException(status_code = 403, detail = 'Users can only delete their own account')
    return users.delete(id)
