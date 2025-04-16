from fastapi import HTTPException

from app.schema.types import User_Type
from app.core.database import get_db_cursor
from app.schema.reviews import Realtor_Reviews

from app.utils.helpers import get_user_type_from_id

def get_one(id: int):
    query = '''
                SELECT * 
                FROM realtor_reviews 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_review = cursor.fetchone()
        if not realtor_review:
            raise HTTPException(status_code = 404, detail = 'Realtor review not found')
        return realtor_review

def get_all():
    query = '''
                SELECT * 
                FROM realtor_reviews 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_reviews = cursor.fetchall()
        return [dict(realtor_review) for realtor_review in realtor_reviews]

def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM realtor_reviews 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_reviews = cursor.fetchall()
        return [dict(realtor_review) for realtor_review in realtor_reviews]

def get_all_by_realtor_user_id(realtor_user_id: int):
    query = '''
                SELECT * 
                FROM realtor_reviews 
                WHERE realtor_user_id = {}
            '''.format(realtor_user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        realtor_reviews = cursor.fetchall()
        return [dict(realtor_review) for realtor_review in realtor_reviews]

def create(realtor_review: Realtor_Reviews):
    user_type = get_user_type_from_id(realtor_review.realtor_user_id)
    if (user_type != User_Type.REALTOR):
        raise HTTPException(status_code = 400, detail = 'Review is not for a realtor')
    query = '''
                INSERT INTO realtor_reviews 
                    (user_id, realtor_user_id, status, rating, review)
                VALUES 
                    ({}, {}, '{}', {}, '{}')
                RETURNING id
            '''.format(
                    realtor_review.user_id, 
                    realtor_review.realtor_user_id,
                    realtor_review.status.value, 
                    realtor_review.rating, 
                    realtor_review.review
                )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            realtor_review_id = cursor.fetchone()
            return dict(realtor_review_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, realtor_review: Realtor_Reviews):
    query = '''
                UPDATE realtor_reviews 
                SET 
                    rating = {}, 
                    review = '{}',
                    status = '{}'
                WHERE id = {}
                AND user_id = {}
                AND realtor_user_id = {}
                RETURNING id, updated_at
            '''.format(
                realtor_review.rating, 
                realtor_review.review, 
                realtor_review.status,
                id, 
                realtor_review.user_id, 
                realtor_review.realtor_user_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            realtor_review = cursor.fetchone()
            return dict(realtor_review)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, user_id: int, realtor_user_id: int):
    query = '''
                DELETE FROM realtor_reviews 
                WHERE id = {}
                AND user_id = {}
                AND realtor_user_id = {}
            '''.format(id, user_id, realtor_user_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Realtor review {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
