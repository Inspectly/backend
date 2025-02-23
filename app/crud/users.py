from fastapi import HTTPException

from app.schema.users import Users
from app.core.database import get_db_cursor
from app.crud.user_types import get_one_user_type

def get_one(id: int):
    query = '''
                SELECT * 
                FROM users 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code = 404, detail = 'User not found')
        return dict(user)

def get_all():
    query = '''
                SELECT * 
                FROM users
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        users = cursor.fetchall()
        return [dict(user) for user in users]
    
def get_one_by_firebase_id(firebase_id: str):
    query = '''
                SELECT * 
                FROM users 
                WHERE firebase_id = '{}'
            '''.format(firebase_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code = 404, detail = 'User not found')
        return dict(user)

def create(user: Users):
    user_type = get_one_user_type(user.user_type.user_type.value)
    if (user_type['user_type'] != user.user_type.user_type.value):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    query = '''
                INSERT INTO users 
                    (user_type, firebase_id)
                VALUES 
                    ('{}', '{}')
                RETURNING id, created_at
            '''.format(
                user.user_type.user_type.value,
                user.firebase_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()
            return dict(user)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, user: Users):
    user_type = get_one_user_type(user.user_type)
    if (user_type != user.user_type):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    query = '''
                UPDATE users 
                SET 
                    user_type = '{}'
                WHERE id = {}
                RETURNING id, user_type, updated_at
            '''.format(
                user.user_type,
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()
            return dict(user)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def delete(id: int):
    query = '''
                DELETE FROM users 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'User {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
