from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.types import User_Types, User_Type

def get_one(id: int):
    query = '''
                SELECT * 
                FROM user_types 
                WHERE id = {}
                LIMIT 1
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_type = cursor.fetchone()
    if not user_type:
        raise HTTPException(status_code = 404, detail = 'User type not found')
    return dict(user_type)

def get_one_user_type(user_type: User_Type):
    query = '''
                SELECT user_type
                FROM user_types 
                WHERE user_type = '{}'
                LIMIT 1
            '''.format(user_type)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_type = cursor.fetchone()
    if not user_type:
        raise HTTPException(status_code = 404, detail = 'User type not found')
    return dict(user_type)

def get_all():
    query = '''
                SELECT * 
                FROM user_types
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_types = cursor.fetchall()
    return [dict(user_type) for user_type in user_types]

def create(user_type: User_Types):
    if not isinstance(user_type.user_type, User_Type):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    query = '''
                INSERT INTO user_types 
                    (user_type)
                VALUES ('{}')
                RETURNING id, user_type, created_at
            '''.format(user_type.user_type.value)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user_type = cursor.fetchone()   
            return dict(user_type)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, user_type: User_Types):
    query = '''
                UPDATE user_types 
                SET user_type = '{}'
                WHERE id = {}
                RETURNING id, user_type, updated_at
            '''.format(user_type, id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user_type = cursor.fetchone()
            return dict(user_type)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    user_type = get_one(id)
    if (not user_type):
        raise HTTPException(status_code = 404, detail = 'User type not found')
    query = '''
                DELETE FROM user_types 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'User type {user_type["user_type"]} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
