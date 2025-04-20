from fastapi import HTTPException

from app.schema.users import Realtors
from app.schema.types import User_Type
from app.core.database import get_db_cursor

from app.utils.helpers import get_user_type_from_id

def get_one(id: int):
    query = '''
                SELECT * 
                FROM realtors 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor = cursor.fetchone()
        if not realtor:
            raise HTTPException(status_code = 404, detail = 'Realtor not found')
        return dict(realtor)

def get_one_realtor_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM realtors 
                WHERE realtor_user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor = cursor.fetchone()
        if not realtor:
            raise HTTPException(status_code = 404, detail = 'Realtor not found')
        return dict(realtor)

def get_all():
    query = '''
                SELECT * 
                FROM realtors 
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtors = cursor.fetchall()
        return [dict(realtor) for realtor in realtors]

def create(realtor: Realtors):
    user_type = get_user_type_from_id(realtor.realtor_user_id)
    if (user_type != User_Type.REALTOR):
        raise HTTPException(status_code = 400, detail = 'User is not a realtor')
    query = '''
                INSERT INTO realtors 
                    (realtor_user_id, realtor_firm_id, first_name, last_name, email, phone, address, city, state, country, postal_code, rating, review)
                VALUES 
                    ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')
                RETURNING id, realtor_user_id, first_name, created_at
            '''.format(
                realtor.realtor_user_id,
                realtor.realtor_firm_id,
                realtor.first_name,
                realtor.last_name,
                realtor.email,
                realtor.phone,
                realtor.address,
                realtor.city,
                realtor.state,
                realtor.country,
                realtor.postal_code,
                realtor.rating,
                realtor.review
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            realtor = cursor.fetchone()
            return dict(realtor)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, realtor: Realtors):
    query = '''
                UPDATE realtors 
                SET  
                    realtor_firm_id = {}, 
                    first_name = '{}', 
                    last_name = '{}', 
                    email = '{}', 
                    phone = '{}', 
                    address = '{}', 
                    city = '{}', 
                    state = '{}', 
                    country = '{}', 
                    postal_code = '{}', 
                    rating = {}, 
                    review = '{}' 
                WHERE id = {}
                AND realtor_user_id = {}
                RETURNING id, realtor_user_id, first_name, updated_at
            '''.format(
                realtor.realtor_firm_id,
                realtor.first_name,
                realtor.last_name,
                realtor.email,
                realtor.phone,
                realtor.address,
                realtor.city,
                realtor.state,
                realtor.country,
                realtor.postal_code,
                realtor.rating,
                realtor.review,
                id,
                realtor.realtor_user_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            realtor = cursor.fetchone()
            return dict(realtor)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, realtor_user_id: int):
    query = '''
                DELETE FROM realtors 
                WHERE id = {}
                AND realtor_user_id = {}
            '''.format(id, realtor_user_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Realtor {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
