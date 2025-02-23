import datetime
from fastapi import HTTPException

from app.schema.types import Login
from app.schema.users import User_Sessions
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM user_sessions 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_session = cursor.fetchone()
        if not user_session:
            raise HTTPException(status_code = 404, detail = 'User session not found')
        return dict(user_session)

def get_user_session(user_id: str):
    query = '''
                SELECT * 
                FROM user_sessions 
                WHERE user_id = '{}'
                AND logout_time IS NULL
                ORDER BY login_time DESC
                LIMIT 1
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_session = cursor.fetchone()
        if not user_session:
            raise HTTPException(status_code = 404, detail = 'User session not found')
        return dict(user_session)

def get_all():
    query = '''
                SELECT * 
                FROM user_sessions
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_sessions = cursor.fetchall()
        return [dict(user_session) for user_session in user_sessions]
    
def create(user_session: User_Sessions):
    if not isinstance(user_session.login, Login):
        raise HTTPException(status_code = 400, detail = 'Invalid login method')
    query = '''
                INSERT INTO user_sessions 
                    (user_id, login, authentication_code)
                VALUES 
                    ({}, '{}', '{}')
                RETURNING id, authentication_code
            '''.format(
                user_session.user_id, 
                user_session.login, 
                user_session.authentication_code
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user_session_id = cursor.fetchone()
            return dict(user_session_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, logout_time: str):
    query = '''
                UPDATE user_sessions 
                SET 
                    logout_time = '{}'
                WHERE id = {}
                RETURNING id
            '''.format(
                logout_time, 
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user_session_id = cursor.fetchone()
            return dict(user_session_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
