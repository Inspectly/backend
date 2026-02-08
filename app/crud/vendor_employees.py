from fastapi import HTTPException

from app.schema.users import Vendor_Employees
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT *
                FROM vendor_employees
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_employee = cursor.fetchone()
    if not vendor_employee:
        raise HTTPException(status_code = 404, detail = 'Vendor employee not found')
    return dict(vendor_employee)

def get_all_by_vendor_id(vendor_id: int):
    query = '''
                SELECT *
                FROM vendor_employees
                WHERE vendor_id = {}
            '''.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_employees = cursor.fetchall()
        return [dict(vendor_employee) for vendor_employee in vendor_employees]

def create(vendor_employee: Vendor_Employees):
    query = '''
                INSERT INTO vendor_employees
                    (vendor_id, first_name, last_name, skills, email, phone, address, city, state, country, postal_code, rating, review, years_of_experience)
                VALUES
                    ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', {})
                RETURNING id, vendor_id, first_name, last_name, created_at
            '''.format(
                vendor_employee.vendor_id,
                vendor_employee.first_name,
                vendor_employee.last_name,
                vendor_employee.skills,
                vendor_employee.email if vendor_employee.email else '',
                vendor_employee.phone if vendor_employee.phone else '',
                vendor_employee.address if vendor_employee.address else '',
                vendor_employee.city,
                vendor_employee.state if vendor_employee.state else '',
                vendor_employee.country if vendor_employee.country else '',
                vendor_employee.postal_code if vendor_employee.postal_code else '',
                vendor_employee.rating if vendor_employee.rating is not None else -1,
                vendor_employee.review if vendor_employee.review else '',
                vendor_employee.years_of_experience if vendor_employee.years_of_experience is not None else 'NULL'
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_employee = cursor.fetchone()
            return dict(vendor_employee)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, vendor_employee: Vendor_Employees):
    query = '''
                UPDATE vendor_employees
                SET
                    first_name = '{}',
                    last_name = '{}',
                    skills = '{}',
                    email = '{}',
                    phone = '{}',
                    address = '{}',
                    city = '{}',
                    state = '{}',
                    country = '{}',
                    postal_code = '{}',
                    rating = {},
                    review = '{}',
                    years_of_experience = {}
                WHERE id = {}
                AND vendor_id = {}
                RETURNING id, vendor_id, first_name, last_name, updated_at
            '''.format(
                vendor_employee.first_name,
                vendor_employee.last_name,
                vendor_employee.skills,
                vendor_employee.email if vendor_employee.email else '',
                vendor_employee.phone if vendor_employee.phone else '',
                vendor_employee.address if vendor_employee.address else '',
                vendor_employee.city,
                vendor_employee.state if vendor_employee.state else '',
                vendor_employee.country if vendor_employee.country else '',
                vendor_employee.postal_code if vendor_employee.postal_code else '',
                vendor_employee.rating if vendor_employee.rating is not None else -1,
                vendor_employee.review if vendor_employee.review else '',
                vendor_employee.years_of_experience if vendor_employee.years_of_experience is not None else 'NULL',
                id,
                vendor_employee.vendor_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_employee = cursor.fetchone()
            return dict(vendor_employee)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, vendor_id: int):
    query = '''
                DELETE FROM vendor_employees
                WHERE id = {}
                AND vendor_id = {}
            '''.format(id, vendor_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Vendor employee {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
