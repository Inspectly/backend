from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.reviews import Vendor_Reviews

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
                    review = '{}'
                WHERE id = {}
                RETURNING id, updated_at
            '''.format(vendor_review.rating, vendor_review.review, id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            vendor_review = cursor.fetchone()
            return dict(vendor_review)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    query = '''
                DELETE FROM vendor_reviews 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Vendor review {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
