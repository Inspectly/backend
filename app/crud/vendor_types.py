from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.types import Vendor_Types, Vendor_Type

def get_one(id: int):
    query = '''
                SELECT * 
                FROM vendor_types 
                WHERE id = {}
                LIMIT 1
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_type = cursor.fetchone()
    if not vendor_type:
        raise HTTPException(status_code = 404, detail = 'Vendor type not found')
    return dict(vendor_type)

def get_one_vendor_type(vendor_type: Vendor_Type):
    query = '''
                SELECT vendor_type
                FROM vendor_types 
                WHERE vendor_type = '{}'
                LIMIT 1
            '''.format(vendor_type)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_type = cursor.fetchone()
    if not vendor_type:
        raise HTTPException(status_code = 404, detail = 'Vendor type not found')
    return dict(vendor_type)

def get_all():
    query = '''
                SELECT * 
                FROM vendor_types
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_types = cursor.fetchall()
    return [dict(vendor_type) for vendor_type in vendor_types]

def create(vendor_type: Vendor_Types):
    if not isinstance(vendor_type.vendor_type, Vendor_Type):
        raise HTTPException(status_code = 400, detail = 'Invalid vendor type')
    query = '''
                INSERT INTO vendor_types 
                    (vendor_type)
                VALUES ('{}')
                RETURNING id, vendor_type, created_at
            '''.format(vendor_type.vendor_type.value)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_type = cursor.fetchone()   
            return dict(vendor_type)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, vendor_type: Vendor_Types):
    query = '''
                UPDATE vendor_types 
                SET vendor_type = '{}'
                WHERE id = {}
                RETURNING id, vendor_type, updated_at
            '''.format(vendor_type, id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_type = cursor.fetchone()
            return dict(vendor_type)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    vendor_type = get_one(id)
    if (not vendor_type):
        raise HTTPException(status_code = 404, detail = 'Vendor type not found')
    query = '''
                DELETE FROM vendor_types 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Vendor type {vendor_type["vendor_type"]} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
