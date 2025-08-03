from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Report_Assessment_Comments

def get_one(id: int):
    query = '''
                SELECT * 
                FROM report_assessment_comments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessment_comment = cursor.fetchone()
        if not report_assessment_comment:
            raise HTTPException(status_code = 404, detail = 'Report assessment comment not found')
        return dict(report_assessment_comment)
    
def get_all():
    query = '''
                SELECT * 
                FROM report_assessment_comments 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessment_comments = cursor.fetchall()
        return [dict(report_assessment_comment) for report_assessment_comment in report_assessment_comments]
    
def get_all_by_report_assessment_id(report_assessment_id: int):
    query = '''
                SELECT * 
                FROM report_assessment_comments 
                WHERE report_assessment_id = {}
            '''.format(report_assessment_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessment_comments = cursor.fetchall()
        return [dict(report_assessment_comment) for report_assessment_comment in report_assessment_comments]
    
def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM report_assessment_comments 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessment_comments = cursor.fetchall()
        return [dict(report_assessment_comment) for report_assessment_comment in report_assessment_comments]
    
def get_comments_by_user_id_and_report_assessment_id(user_id: int, report_assessment_id: int):
    query = '''
                SELECT * 
                FROM report_assessment_comments 
                WHERE user_id = {} AND report_assessment_id = {}
            '''.format(user_id, report_assessment_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessment_comments = cursor.fetchall()
        return [dict(report_assessment_comment) for report_assessment_comment in report_assessment_comments]
    
def create(report_assessment_comment: Report_Assessment_Comments):
    query = '''
                INSERT INTO report_assessment_comments 
                    (report_assessment_id, user_id, comment)
                VALUES 
                    ({}, {}, '{}')
                RETURNING id, created_at, updated_at    
            '''.format(
                report_assessment_comment.report_assessment_id,
                report_assessment_comment.user_id,
                report_assessment_comment.comment
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_assessment_comment_id = cursor.fetchone()
            return dict(report_assessment_comment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, report_assessment_comment: Report_Assessment_Comments):
    query = '''
                UPDATE report_assessment_comments 
                SET 
                    comment = '{}'
                WHERE id = {}
            '''.format(report_assessment_comment.comment, id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_assessment_comment_id = cursor.fetchone()
            return dict(report_assessment_comment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def delete(id: int, report_assessment_id: int):
    query = '''
                DELETE FROM report_assessment_comments 
                WHERE id = {}
                AND report_assessment_id = {}
            '''.format(id, report_assessment_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': 'Report assessment comment deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
