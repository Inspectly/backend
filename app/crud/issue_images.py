from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Issue_Images

def get_one(id: int):
    query = '''
                SELECT *
                FROM issue_images
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_image = cursor.fetchone()
        if not issue_image:
            raise HTTPException(status_code = 404, detail = 'Issue image not found')
        return dict(issue_image)

def get_issue_image(issue_id: int, image_id: int):
    query = '''
                SELECT *
                FROM issue_images
                WHERE issue_id = {} AND id = {}
            '''.format(issue_id, image_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_image = cursor.fetchone()
        if not issue_image:
            raise HTTPException(status_code = 404, detail = 'Issue image not found')
        return dict(issue_image)

def get_issue_images(issue_id: int):
    query = '''
                SELECT *
                FROM issue_images
                WHERE issue_id = {}
            '''.format(issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_images = cursor.fetchall()
        return [dict(image) for image in issue_images]

def create(issue_image: Issue_Images):
    query = '''
                INSERT INTO issue_images
                    (issue_id, url)
                VALUES
                    ({}, '{}')
                RETURNING id, issue_id
            '''.format(issue_image.issue_id, issue_image.url)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_image = cursor.fetchone()
        return dict(issue_image)

def delete(id: int):
    query = '''
                DELETE FROM issue_images
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Issue image {id} deleted successfully'}
