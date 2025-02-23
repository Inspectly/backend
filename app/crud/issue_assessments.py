from fastapi import HTTPException

from app.schema.properties import Issue_Assessments
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM issue_assessments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessment = cursor.fetchone()
        if not issue_assessment:
            raise HTTPException(status_code = 404, detail = 'Issue assessment not found')
        return dict(issue_assessment)
    
def get_all():
    query = '''
                SELECT * 
                FROM issue_assessments 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessments = cursor.fetchall()
        return [dict(issue_assessment) for issue_assessment in issue_assessments]
    
def get_all_by_issue_id(issue_id: int):
    query = '''
                SELECT * 
                FROM issue_assessments 
                WHERE issue_id = {}
            '''.format(issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessments = cursor.fetchall()
        return [dict(issue_assessment) for issue_assessment in issue_assessments]
    
def get_all_by_vendor_id(vendor_id: int, issue_id: int):
    query = '''
                SELECT * 
                FROM issue_assessments 
                WHERE vendor_id = {} AND issue_id = {}
            '''.format(vendor_id, issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessments = cursor.fetchall()
        return [dict(issue_assessment) for issue_assessment in issue_assessments]
    
def create(issue_assessment: Issue_Assessments):
    query = '''
                INSERT INTO issue_assessments 
                    (issue_id, vendor_id, date, status, comment_vendor, comment_client)
                VALUES 
                    ({}, {}, '{}', '{}', '{}', '{}')
                RETURNING id, created_at, updated_at
            '''.format(
                issue_assessment.issue_id,
                issue_assessment.vendor_id,
                issue_assessment.date,
                issue_assessment.status,
                issue_assessment.comment_vendor,
                issue_assessment.comment_client
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_assessment_id = cursor.fetchone()
            return dict(issue_assessment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, issue_assessment: Issue_Assessments):
    query = '''
                UPDATE issue_assessments 
                SET 
                    issue_id = {}, 
                    vendor_id = {}, 
                    date = '{}', 
                    status = '{}', 
                    comment_vendor = '{}', 
                    comment_client = '{}'
                WHERE id = {}
                RETURNING id, updated_at
            '''.format(
                issue_assessment.issue_id,
                issue_assessment.vendor_id,
                issue_assessment.date,
                issue_assessment.status,
                issue_assessment.comment_vendor,
                issue_assessment.comment_client,
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_assessment_id = cursor.fetchone()
            return dict(issue_assessment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    query = '''
                DELETE FROM issue_assessments 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Issue assessment {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
