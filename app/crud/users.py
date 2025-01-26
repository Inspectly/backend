from fastapi import HTTPException

from app.schema.users import Users
from app.core.database import get_db_cursor
from app.crud.user_types import get_one_user_type

def get_one(id: int):
    query = """
                SELECT * 
                FROM users 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code = 404, detail = 'User not found')
        return dict(user)

def get_all():
    query = """
                SELECT * 
                FROM users
                ORDER BY id DESC
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        users = cursor.fetchall()
        return [dict(user) for user in users]

def create(user: Users):
    user_type = get_one_user_type(user.user_type)
    if (user_type != user.user_type):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    if(len(user.user_code) != 5):
        raise HTTPException(status_code = 400, detail = 'Invalid user code')
    query = """
                INSERT INTO users 
                    (user_type, name, email, phone, address, user_code, city, state, country, postal_code)
                VALUES 
                    ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id
            """.format(
                user.user_type, 
                user.name, 
                user.email, 
                user.phone, 
                user.address, 
                user.user_code, 
                user.city, 
                user.state, 
                user.country, 
                user.postal_code
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_id = cursor.fetchone()
        return dict(user_id)
    
def update(id: int, user: Users):
    user_type = get_one_user_type(user.user_type)
    if (user_type != user.user_type):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    if(len(user.user_code) != 5):
        raise HTTPException(status_code = 400, detail = 'Invalid user code')
    query = """
                UPDATE users 
                SET 
                    user_type = '{}',
                    name = '{}',
                    email = '{}',
                    phone = '{}',
                    address = '{}',
                    user_code = '{}',
                    city = '{}',
                    state = '{}',
                    country = '{}',
                    postal_code = '{}'
                WHERE id = {}
                RETURNING id
            """.format(
                user.user_type,
                user.name, 
                user.email, 
                user.phone, 
                user.address, 
                user.user_code, 
                user.city, 
                user.state, 
                user.country, 
                user.postal_code, 
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_id = cursor.fetchone()
        return dict(user_id)
    
def delete(id: int):
    query = """
                DELETE FROM users 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'User {id} deleted successfully'}
