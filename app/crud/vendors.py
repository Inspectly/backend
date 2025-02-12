from fastapi import HTTPException

from app.schema.users import Vendors
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM vendors 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor = cursor.fetchone()
        return dict(vendor)

def get_all():
    query = '''
                SELECT * 
                FROM vendors 
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendors = cursor.fetchall()
        return [dict(vendor) for vendor in vendors]

def create(vendor: Vendors):
    query = '''
                INSERT INTO vendors 
                    (vendor_user_id, vendor_type, code, name, email, phone, address, city, state, country, postal_code, rating, review)
                VALUES 
                    ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')
                RETURNING id, vendor_user_id, first_name, created_at
            '''.format(
                vendor.vendor_user_id,
                vendor.vendor_type,
                vendor.code,
                vendor.name,
                vendor.email,
                vendor.phone,
                vendor.address,
                vendor.city,
                vendor.state,
                vendor.country,
                vendor.postal_code,
                vendor.rating,
                vendor.review
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor = cursor.fetchone()
        return dict(vendor)
    
def update(id: int, vendor: Vendors):
    query = '''
                UPDATE vendors 
                SET 
                    vendor_user_id = '{}', 
                    vendor_type = '{}', 
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
                RETURNING id, vendor_user_id, first_name, updated_at
            '''.format(
                vendor.vendor_user_id,
                vendor.vendor_type,
                vendor.code,
                vendor.name,
                vendor.email,
                vendor.phone,
                vendor.address,
                vendor.city,
                vendor.state,
                vendor.country,
                vendor.postal_code,
                vendor.rating,
                vendor.review,
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor = cursor.fetchone()
        return dict(vendor)

def delete(id: int):
    query = '''
                DELETE FROM vendors 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Vendor {id} deleted successfully'}
