from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.crud.user_types import get_one_user_type
from app.schema.properties import Issue_Assessments

from app.utils.helpers import get_uuid

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
    
def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM issue_assessments 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessments = cursor.fetchall()
        return [dict(issue_assessment) for issue_assessment in issue_assessments]
    
def get_all_by_interaction_id(interaction_id: str):
    interaction_id = get_uuid(interaction_id)
    query = '''
                SELECT * 
                FROM issue_assessments 
                WHERE interaction_id = '{}'
                ORDER BY id DESC
            '''.format(interaction_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_assessments = cursor.fetchall()
        return [dict(issue_assessment) for issue_assessment in issue_assessments]
    
def create(issue_assessment: Issue_Assessments):
    interaction_id = get_uuid(issue_assessment.interaction_id)
    user_type = get_one_user_type(issue_assessment.user_type.user_type.value)
    if (user_type['user_type'] != issue_assessment.user_type.user_type.value):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    query = '''
                INSERT INTO issue_assessments 
                    (issue_id, user_id, interaction_id, user_type, start_time, end_time, status, min_assessment_time)
                VALUES 
                    ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, created_at, updated_at
            '''.format(
                issue_assessment.issue_id,
                issue_assessment.user_id,
                interaction_id,
                issue_assessment.user_type,
                issue_assessment.start_time,
                issue_assessment.end_time,
                issue_assessment.status,
                issue_assessment.min_assessment_time
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_assessment_id = cursor.fetchone()
            return dict(issue_assessment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, issue_assessment: Issue_Assessments):
    interaction_id = get_uuid(issue_assessment.interaction_id)
    query = '''
                UPDATE issue_assessments 
                SET 
                    start_time = '{}', 
                    end_time = '{}', 
                    status = '{}', 
                    min_assessment_time = '{}'
                WHERE id = {}
                AND issue_id = {}
                AND interaction_id = '{}'
                RETURNING id, updated_at
            '''.format(
                issue_assessment.start_time,
                issue_assessment.end_time,
                issue_assessment.status,
                issue_assessment.min_assessment_time,
                id,
                issue_assessment.issue_id,
                interaction_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_assessment_id = cursor.fetchone()
            return dict(issue_assessment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, issue_id: int, interaction_id: str):
    query = '''
                DELETE FROM issue_assessments 
                WHERE id = {}
                AND issue_id = {}
                AND interaction_id = '{}'
            '''.format(id, issue_id, interaction_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Issue assessment {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
