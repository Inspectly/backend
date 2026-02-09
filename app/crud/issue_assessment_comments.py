from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Issue_Assessment_Comments

def get_one(id: int):
    query = '''
                SELECT * 
                FROM issue_assessment_comments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessment_comment = cursor.fetchone()
        if not issue_assessment_comment:
            raise HTTPException(status_code = 404, detail = 'Issue assessment comment not found')
        return dict(issue_assessment_comment)
    
def get_all():
    query = '''
                SELECT * 
                FROM issue_assessment_comments 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessment_comments = cursor.fetchall()
        return [dict(issue_assessment_comment) for issue_assessment_comment in issue_assessment_comments]
    
def get_all_by_issue_assessment_id(issue_assessment_id: int):
    query = '''
                SELECT * 
                FROM issue_assessment_comments 
                WHERE issue_assessment_id = {}
            '''.format(issue_assessment_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessment_comments = cursor.fetchall()
        return [dict(issue_assessment_comment) for issue_assessment_comment in issue_assessment_comments]
    
def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM issue_assessment_comments 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessment_comments = cursor.fetchall()
        return [dict(issue_assessment_comment) for issue_assessment_comment in issue_assessment_comments]
    
def get_comments_by_user_id_and_issue_assessment_id(user_id: int, issue_assessment_id: int):
    query = '''
                SELECT * 
                FROM issue_assessment_comments 
                WHERE user_id = {} AND issue_assessment_id = {}
            '''.format(user_id, issue_assessment_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessment_comments = cursor.fetchall()
        return [dict(issue_assessment_comment) for issue_assessment_comment in issue_assessment_comments]
    
def create(issue_assessment_comment: Issue_Assessment_Comments):
    query = '''
                INSERT INTO issue_assessment_comments
                    (issue_assessment_id, user_id, comment)
                VALUES
                    (%s, %s, %s)
                RETURNING id, created_at, updated_at
            '''
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                issue_assessment_comment.issue_assessment_id,
                issue_assessment_comment.user_id,
                issue_assessment_comment.comment
            ))
            issue_assessment_comment_id = cursor.fetchone()
            return dict(issue_assessment_comment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, issue_assessment_comment: Issue_Assessment_Comments):
    query = '''
                UPDATE issue_assessment_comments
                SET
                    comment = %s
                WHERE id = %s
            '''
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (issue_assessment_comment.comment, id))
            issue_assessment_comment_id = cursor.fetchone()
            return dict(issue_assessment_comment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def delete(id: int, issue_assessment_id: int):
    query = '''
                DELETE FROM issue_assessment_comments 
                WHERE id = {}
                AND issue_assessment_id = {}
            '''.format(id, issue_assessment_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': 'Issue assessment comment deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
