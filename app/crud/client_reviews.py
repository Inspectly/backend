from fastapi import HTTPException

from app.schema.types import User_Type
from app.core.database import get_db_cursor
from app.schema.reviews import Client_Reviews

from app.utils.helpers import get_user_type_from_id

def get_one(id: int):
    query = '''
                SELECT * 
                FROM client_reviews 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client_review = cursor.fetchone()
        if not client_review:
            raise HTTPException(status_code = 404, detail = 'Client review not found')
        return client_review

def get_all():
    query = '''
                SELECT * 
                FROM client_reviews 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client_reviews = cursor.fetchall()
        return [dict(client_review) for client_review in client_reviews]

def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM client_reviews 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client_reviews = cursor.fetchall()
        return [dict(client_review) for client_review in client_reviews]

def get_all_by_client_user_id(client_user_id: int):
    query = '''
                SELECT * 
                FROM client_reviews 
                WHERE client_user_id = {}
            '''.format(client_user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client_reviews = cursor.fetchall()
        return [dict(client_review) for client_review in client_reviews]

def create(client_review: Client_Reviews):
    user_type = get_user_type_from_id(client_review.client_user_id)
    if (user_type != User_Type.CLIENT):
        raise HTTPException(status_code = 400, detail = 'Review is not for a client')
    query = '''
                INSERT INTO client_reviews 
                    (user_id, client_user_id, status, rating, review)
                VALUES 
                    ({}, {}, '{}', {}, '{}')
                RETURNING id
            '''.format(
                    client_review.user_id, 
                    client_review.client_user_id,
                    client_review.status.value, 
                    client_review.rating, 
                    client_review.review
                )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            client_review_id = cursor.fetchone()
            return dict(client_review_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, client_review: Client_Reviews):
    query = '''
                UPDATE client_reviews 
                SET 
                    rating = {}, 
                    review = '{}',
                    status = '{}'
                WHERE id = {}
                AND user_id = {}
                AND client_user_id = {}
                RETURNING id, updated_at
            '''.format(
                client_review.rating, 
                client_review.review, 
                client_review.status,
                id, 
                client_review.user_id, 
                client_review.client_user_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            client_review = cursor.fetchone()
            return dict(client_review)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, user_id: int, client_user_id: int):
    query = '''
                DELETE FROM client_reviews 
                WHERE id = {}
                AND user_id = {}
                AND client_user_id = {}
            '''.format(id, user_id, client_user_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Client review {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
