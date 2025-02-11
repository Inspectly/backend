from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.users import User_Logins

def get_one(id: int):
    query = """
                SELECT * 
                FROM user_logins 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_login = cursor.fetchone()
        if not user_login:
            raise HTTPException(status_code = 404, detail = 'User login not found')
        return dict(user_login)

def get_user_login(user_id: str):
    query = """
                SELECT * 
                FROM user_logins 
                WHERE user_id = '{}'
            """.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_login = cursor.fetchone()
        if not user_login:
            raise HTTPException(status_code = 404, detail = 'User login not found')
        return dict(user_login)

def get_all():
    query = """
                SELECT * 
                FROM user_logins
                ORDER BY id DESC
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_logins = cursor.fetchall()
        return [dict(user_login) for user_login in user_logins]

def create(user_login: User_Logins):
    query = """
                INSERT INTO user_logins 
                    (user_id, email_login, email, phone_login, phone, gmail_login, gmail)
                VALUES 
                    ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, created_at
            """.format(
                user_login.user_id, 
                user_login.email_login, 
                user_login.email, 
                user_login.phone_login, 
                user_login.phone, 
                user_login.gmail_login, 
                user_login.gmail
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_login_id = cursor.fetchone()
        return dict(user_login_id)
    
def update(id: int, user_login: User_Logins):
    query = """
                UPDATE user_logins 
                SET 
                    email_login = '{}', 
                    email = '{}', 
                    phone_login = '{}', 
                    phone = '{}', 
                    gmail_login = '{}', 
                    gmail = '{}'
                WHERE id = {}
                RETURNING id, updated_at
            """.format(
                user_login.email_login, 
                user_login.email, 
                user_login.phone_login, 
                user_login.phone, 
                user_login.gmail_login, 
                user_login.gmail, 
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_login_id = cursor.fetchone()
        return dict(user_login_id)

def delete(id: int):
    query = """
                DELETE FROM user_logins 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'User login {id} deleted successfully'}
