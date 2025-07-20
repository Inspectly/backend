from fastapi import HTTPException

from app.schema.users import Vendors
from app.schema.types import User_Type
from app.core.database import get_db_cursor
from app.crud.vendor_types import get_one_vendor_type

from app.utils.helpers import get_user_type_from_id

def get_one(id: int): 
    query = '''
                SELECT * 
                FROM vendors 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor = cursor.fetchone()
    if not vendor:
        raise HTTPException(status_code = 404, detail = 'Vendor not found')
    return dict(vendor)

def get_one_vendor_user_id(vendor_user_id: int):
    query = '''
                SELECT * 
                FROM vendors 
                WHERE vendor_user_id = {}
            '''.format(vendor_user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor = cursor.fetchone()
    if not vendor:
        raise HTTPException(status_code = 404, detail = 'Vendor not found')
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
    user_type = get_user_type_from_id(vendor.vendor_user_id)
    if (user_type != User_Type.VENDOR):
        raise HTTPException(status_code = 400, detail = 'User is not a vendor')
    
    if (len(vendor.code) != 5):
        raise HTTPException(status_code = 400, detail = 'Invalid Vendor Code')
    
    valid_vendor_type = get_one_vendor_type(vendor.vendor_type.vendor_type.value)
    if not valid_vendor_type:
        raise HTTPException(status_code = 400, detail = f'Invalid main vendor type {vendor.vendor_type.vendor_type.value} does not exist')
    
    vendor_types = vendor.vendor_types.split(',')
    for vendor_type in vendor_types:
        vendor_type = vendor_type.strip().lower()
        additional_vendor_type = get_one_vendor_type(vendor_type)
        if (additional_vendor_type['vendor_type'] != vendor_type):
            raise HTTPException(status_code = 400, detail = f'Invalid additional vendor type {vendor_type} does not exist')
    
    query = '''
                INSERT INTO vendors 
                    (vendor_user_id, vendor_type, vendor_types, code, name, email, phone, address, city, state, country, postal_code, rating, review)
                VALUES 
                    ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')
                RETURNING id, vendor_user_id, code, name, created_at
            '''.format(
                vendor.vendor_user_id,
                vendor.vendor_type.vendor_type.value,
                vendor.vendor_types,
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
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor = cursor.fetchone()
            return dict(vendor)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, vendor: Vendors):
    if (len(vendor.code) != 5):
        raise HTTPException(status_code = 400, detail = 'Invalid Vendor Code')
    
    valid_vendor_type = get_one_vendor_type(vendor.vendor_type.vendor_type.value)
    if not valid_vendor_type:
        raise HTTPException(status_code = 400, detail = f'Invalid main vendor type {vendor.vendor_type.vendor_type.value} does not exist')
    
    vendor_types = vendor.vendor_types.split(',')
    for vendor_type in vendor_types:
        vendor_type = vendor_type.strip().lower()
        additional_vendor_type = get_one_vendor_type(vendor_type)
        if (additional_vendor_type['vendor_type'] != vendor_type):
            raise HTTPException(status_code = 400, detail = f'Invalid additional vendor type {vendor_type} does not exist')
    
    query = '''
                UPDATE vendors 
                SET  
                    vendor_type = '{}', 
                    vendor_types = '{}', 
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
                AND vendor_user_id = {}
                RETURNING id, vendor_user_id, code, name, updated_at
            '''.format(
                vendor.vendor_type.vendor_type.value,
                vendor.vendor_types,
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
                id,
                vendor.vendor_user_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor = cursor.fetchone()
            return dict(vendor)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, vendor_user_id: int):
    query = '''
                DELETE FROM vendors 
                WHERE id = {}
                AND vendor_user_id = {}
            '''.format(id, vendor_user_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Vendor {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
