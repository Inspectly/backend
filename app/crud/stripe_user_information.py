from fastapi import HTTPException
import stripe

from app.core.database import get_db_cursor
from app.schema.payments import User_Stripe_Information

def get_one(id: int):
    query = '''
                SELECT * 
                FROM user_stripe_information 
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
                FROM user_stripe_information
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        user_stripe_information = cursor.fetchall()
        return [dict(user_stripe_information) for user_stripe_information in user_stripe_information]
    
def get_user_stripe_information(user_id: int):
    query = '''
                SELECT * 
                FROM user_stripe_information 
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
                FROM user_stripe_information 
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
                INSERT INTO user_stripe_information 
                    (user_id, stripe_user_id)
                VALUES 
                    ({}, '{}')
                RETURNING id, user_id
            '''.format(
                user_stripe_information.user_id,
                user_stripe_information.stripe_user_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user_stripe_information_id = cursor.fetchone()
            return dict(user_stripe_information_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def create_stripe_existing_user(user_id: int):
    query = '''
                SELECT firebase_id, user_type
                FROM users
                WHERE id = {}
            '''.format(user_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail='User not found')

            customer = stripe.Customer.create(
                metadata={
                    "app_user_id": str(user_id),
                    "firebase_id": user['firebase_id'] or "",
                    "user_type": user['user_type'] or "",
                },
            )

            create(
                User_Stripe_Information(
                    user_id=user_id,
                    stripe_user_id=customer.id
                )
            )

            return {"user_id": user_id, "stripe_customer_id": customer.id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def update(id: int, user_stripe_information: User_Stripe_Information):
    query = '''
                UPDATE user_stripe_information 
                    SET 
                        user_id = {}, 
                        stripe_user_id = '{}'
                WHERE id = {}
                RETURNING id, user_id, stripe_user_id, updated_at
            '''.format(
                user_stripe_information.user_id, 
                user_stripe_information.stripe_user_id, 
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': 'User Stripe Information updated successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    query = '''
                DELETE FROM user_stripe_information 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': 'User Stripe Information deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
