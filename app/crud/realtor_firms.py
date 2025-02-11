from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.realtor_firms import Realtor_Firms

def get_one(id: int):
    query = """
                SELECT * 
                FROM realtor_firms 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_firm = cursor.fetchone()
        if not realtor_firm:
            raise HTTPException(status_code = 404, detail = 'Realtor firm not found')
        return dict(realtor_firm)

def get_all():
    query = """
                SELECT * 
                FROM realtor_firms
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_firms = cursor.fetchall()
        return [dict(realtor_firm) for realtor_firm in realtor_firms]

def create(realtor_firm: Realtor_Firms):
    query = """
                INSERT INTO realtor_firms 
                    (code, name, email, phone, address, city, state, country, postal_code, rating, review)
                VALUES 
                    ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')
                RETURNING id, code, name, created_at
            """.format(
                realtor_firm.code,
                realtor_firm.name,
                realtor_firm.email,
                realtor_firm.phone,
                realtor_firm.address,
                realtor_firm.city,
                realtor_firm.state,
                realtor_firm.country,
                realtor_firm.postal_code,
                realtor_firm.rating,
                realtor_firm.review
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_firm = cursor.fetchone()
        return dict(realtor_firm)

def update(id: int, realtor_firm: Realtor_Firms):
    query = """
                UPDATE realtor_firms 
                SET 
                    code = '{}', 
                    name = '{}', 
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
                RETURNING id, code, name, updated_at
            """.format(
                realtor_firm.code,
                realtor_firm.name,
                realtor_firm.email,
                realtor_firm.phone,
                realtor_firm.address,
                realtor_firm.city,
                realtor_firm.state,
                realtor_firm.country,
                realtor_firm.postal_code,
                realtor_firm.rating,
                realtor_firm.review,
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_firm = cursor.fetchone()
        return dict(realtor_firm)

def delete(id: int):
    query = """
                DELETE FROM realtor_firms 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Realtor firm {id} deleted successfully'}
