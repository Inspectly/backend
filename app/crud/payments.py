from fastapi import HTTPException

from app.schema.payments import Payments
from app.core.database import get_db_cursor

def get_one(id: int):
    query = """
                SELECT * 
                FROM payments 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        payment = cursor.fetchone()
        if not payment:
            raise HTTPException(status_code = 404, detail = 'Payment not found')
        return dict(payment)
    
def get_all():
    query = """
                SELECT * 
                FROM payments
                ORDER BY id DESC
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        payments = cursor.fetchall()
        return [dict(payment) for payment in payments]

def get_user_payments(user_id: int):
    query = """
                SELECT * 
                FROM payments 
                WHERE user_id = {}
            """.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        payments = cursor.fetchall()
        return [dict(payment) for payment in payments]

def create(payment: Payments):
    query = """
                INSERT INTO payments 
                    (user_id, payment_amount)
                VALUES 
                    ({}, {})
                RETURNING id
            """.format(payment.user_id, payment.payment_amount)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        payment_id = cursor.fetchone()
        return dict(payment_id)
    
def delete(id: int):
    query = """
                DELETE FROM payments 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Payment {id} deleted successfully'}
