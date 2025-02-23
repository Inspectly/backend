from fastapi import HTTPException

from app.schema.properties import Comments
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM comments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        comment = cursor.fetchone()
        if not comment:
            raise HTTPException(status_code = 404, detail = 'Comment not found')
        return dict(comment)
    
def get_all():
    query = '''
                SELECT * 
                FROM comments 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        comments = cursor.fetchall()
        return [dict(comment) for comment in comments]

def get_issue_comments(issue_id: int):
    query = '''
                SELECT * 
                FROM comments 
                WHERE issue_id = {}
            '''.format(issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        comments = cursor.fetchall()
        return [dict(comment) for comment in comments]

def get_user_comments(user_id: int):
    query = '''
                SELECT * 
                FROM comments 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        comments = cursor.fetchall()
        return [dict(comment) for comment in comments]

def create(comment: Comments):
    query = '''
                INSERT INTO comments (issue_id, user_id, comment)
                VALUES ({}, {}, '{}')
                RETURNING id, issue_id, user_id, created_at
            '''.format(
                comment.issue_id,
                comment.user_id,
                comment.comment
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            comment = cursor.fetchone()
            return dict(comment)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, comment: Comments):
    query = '''
                UPDATE comments 
                SET comment = '{}'
                WHERE id = {}
                RETURNING id, issue_id, user_id, updated_at
            '''.format(comment.comment, id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            comment = cursor.fetchone()
            return dict(comment)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def delete(id: int):
    query = '''
                DELETE FROM comments 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Comment {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
