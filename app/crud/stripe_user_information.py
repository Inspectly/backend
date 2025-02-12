from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.payments import User_Stripe_Information

def get_one(id: int):
    query = '''
                SELECT * 
                FROM stripe_user_information 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_stripe_information = cursor.fetchone()
        if not user_stripe_information:
            raise HTTPException(status_code = 404, detail = 'User Stripe Information not found')
        return dict(user_stripe_information)
    
def get_all():
    query = '''
                SELECT * 
                FROM stripe_user_information
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_stripe_information = cursor.fetchall()
        return [dict(user_stripe_information) for user_stripe_information in user_stripe_information]
    
def get_user_stripe_information(user_id: int):
    query = '''
                SELECT * 
                FROM stripe_user_information 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_stripe_information = cursor.fetchone()
        if not user_stripe_information:
            raise HTTPException(status_code = 404, detail = 'User Stripe Information not found')
        return dict(user_stripe_information)
    
def get_user_stripe_information_by_stripe_user_id(stripe_user_id: str):
    query = '''
                SELECT * 
                FROM stripe_user_information 
                WHERE stripe_user_id = {}
            '''.format(stripe_user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_stripe_information = cursor.fetchone()
        if not user_stripe_information:
            raise HTTPException(status_code = 404, detail = 'User Stripe Information not found')
        return dict(user_stripe_information) 
    
def create(user_stripe_information: User_Stripe_Information):
    query = '''
                INSERT INTO stripe_user_information 
                    (user_id, stripe_user_id)
                VALUES 
                    ({}, {})
            '''.format(
                user_stripe_information.user_id,
                user_stripe_information.stripe_user_id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_stripe_information_id = cursor.fetchone()
        return dict(user_stripe_information_id)
    
def update(id: int, user_stripe_information: User_Stripe_Information):
    query = '''
                UPDATE stripe_user_information 
                    SET 
                        user_id = {}, 
                        stripe_user_id = {}
                WHERE id = {}
                RETURNING id, user_id, stripe_user_id, updated_at
            '''.format(
                user_stripe_information.user_id, 
                user_stripe_information.stripe_user_id, 
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': 'User Stripe Information updated successfully'}

def delete(id: int):
    query = '''
                DELETE FROM stripe_user_information 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': 'User Stripe Information deleted successfully'}