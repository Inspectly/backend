from fastapi import HTTPException

from app.schema.users import Realtors
from app.core.database import get_db_cursor

def get_one(id: int):
    query = """
                SELECT * 
                FROM realtors 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor = cursor.fetchone()
        if not realtor:
            raise HTTPException(status_code = 404, detail = 'Realtor not found')
        return dict(realtor)

def get_all():
    query = """
                SELECT * 
                FROM realtors 
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtors = cursor.fetchall()
        return [dict(realtor) for realtor in realtors]

def create(realtor: Realtors):
    query = """
                INSERT INTO realtors 
                    (realtor_user_id, realtor_firm_id, first_name, last_name, email, phone, address, city, state, country, postal_code, rating, review)
                VALUES 
                    ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')
                RETURNING id, realtor_user_id, first_name, created_at
            """.format(
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
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor = cursor.fetchone()
        return dict(realtor)

def update(id: int, realtor: Realtors):
    query = """
                UPDATE realtors 
                SET 
                    realtor_user_id = '{}', 
                    realtor_firm_id = '{}', 
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
                RETURNING id, realtor_user_id, first_name, updated_at
            """.format(
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
                realtor.review,
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor = cursor.fetchone()
        return dict(realtor)

def delete(id: int):
    query = """
                DELETE FROM realtors 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Realtor {id} deleted successfully'}
