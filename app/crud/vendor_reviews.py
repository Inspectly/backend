from fastapi import HTTPException

from app.schema.types import User_Type
from app.core.database import get_db_cursor
from app.schema.reviews import Vendor_Reviews

from app.utils.helpers import get_user_type_from_id

def get_one(id: int):
    query = '''
                SELECT * 
                FROM vendor_reviews 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_review = cursor.fetchone()
        if not vendor_review:
            raise HTTPException(status_code = 404, detail = 'Vendor review not found')
        return vendor_review

def get_all():
    query = '''
                SELECT * 
                FROM vendor_reviews 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_reviews = cursor.fetchall()
        return [dict(vendor_review) for vendor_review in vendor_reviews]

def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM vendor_reviews 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_reviews = cursor.fetchall()
        return [dict(vendor_review) for vendor_review in vendor_reviews]

def get_all_by_vendor_user_id(vendor_user_id: int):
    query = '''
                SELECT * 
                FROM vendor_reviews 
                WHERE vendor_user_id = {}
            '''.format(vendor_user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        vendor_reviews = cursor.fetchall()
        return [dict(vendor_review) for vendor_review in vendor_reviews]

def create(vendor_review: Vendor_Reviews):
    user_type = get_user_type_from_id(vendor_review.vendor_user_id)
    if (user_type != User_Type.VENDOR):
        raise HTTPException(status_code = 400, detail = 'Review is not for a vendor')
    query = '''
                INSERT INTO vendor_reviews 
                    (user_id, vendor_user_id, rating, review)
                VALUES 
                    ({}, {}, {}, '{}')
                RETURNING id
            '''.format(
                    vendor_review.user_id, 
                    vendor_review.vendor_user_id, 
                    vendor_review.rating, 
                    vendor_review.review
                )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_review_id = cursor.fetchone()
            return dict(vendor_review_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, vendor_review: Vendor_Reviews):
    query = '''
                UPDATE vendor_reviews 
                SET 
                    rating = {}, 
                    review = '{}',
                    status = '{}'
                WHERE id = {}
                AND user_id = {}
                AND vendor_user_id = {}
                RETURNING id, updated_at
            '''.format(
                    vendor_review.rating, 
                    vendor_review.review, 
                    vendor_review.status,
                    id, 
                    vendor_review.user_id, 
                    vendor_review.vendor_user_id
                )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_review = cursor.fetchone()
            return dict(vendor_review)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, user_id: int, vendor_user_id: int):
    query = '''
                DELETE FROM vendor_reviews 
                WHERE id = {}
                AND user_id = {}
                AND vendor_user_id = {}
            '''.format(id, user_id, vendor_user_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Vendor review {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
