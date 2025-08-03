from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.crud.user_types import get_one_user_type
from app.schema.properties import Report_Assessments

from app.utils.helpers import get_uuid

def get_one(id: int):
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessment = cursor.fetchone()
        if not report_assessment:
            raise HTTPException(status_code = 404, detail = 'Report assessment not found')
        return dict(report_assessment)
    
def get_all():
    query = '''
                SELECT * 
                FROM report_assessments 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
    
def get_all_by_report_id(report_id: int):
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE report_id = {}
            '''.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
    
def get_all_by_user_id(user_id: int):
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
    
def get_all_by_interaction_id(interaction_id: str):
    transformed_interaction_id = get_uuid(interaction_id)
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE interaction_id = '{}'
                ORDER BY id DESC
            '''.format(transformed_interaction_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
    
def get_all_by_users_interaction_id(users_interaction_id: str):
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE users_interaction_id = '{}'
                ORDER BY id DESC
            '''.format(users_interaction_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
    
def get_all_by_client_id_users_interaction_id(client_id: int):
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE users_interaction_id LIKE '{}_%'
            '''.format(client_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
    
def get_all_by_vendor_id_users_interaction_id(vendor_id: int):
    query = '''
                SELECT * 
                FROM report_assessments 
                WHERE users_interaction_id LIKE '%_{}'
            '''.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_assessments = cursor.fetchall()
        return [dict(report_assessment) for report_assessment in report_assessments]
                
def create(report_assessment: Report_Assessments):
    transformed_interaction_id = get_uuid(report_assessment.interaction_id)
    user_type = get_one_user_type(report_assessment.user_type.value)
    if (user_type['user_type'] != report_assessment.user_type.value):
        raise HTTPException(status_code = 400, detail = 'Invalid user type')
    query = '''
                INSERT INTO report_assessments 
                    (report_id, user_id, interaction_id, users_interaction_id, user_type, start_time, end_time, status, min_assessment_time)
                VALUES 
                    ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, created_at, updated_at
            '''.format(
                report_assessment.report_id,
                report_assessment.user_id,
                transformed_interaction_id,
                report_assessment.users_interaction_id,
                report_assessment.user_type.value,
                report_assessment.start_time,
                report_assessment.end_time,
                report_assessment.status,
                report_assessment.min_assessment_time
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_assessment_id = cursor.fetchone()
            return dict(report_assessment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, report_assessment: Report_Assessments):
    transformed_interaction_id = get_uuid(report_assessment.interaction_id)
    query = '''
                UPDATE report_assessments 
                SET 
                    start_time = '{}', 
                    end_time = '{}', 
                    status = '{}', 
                    min_assessment_time = '{}',
                    user_last_viewed = '{}'
                WHERE id = {}
                AND report_id = {}
                AND interaction_id = '{}'
                RETURNING id, updated_at
            '''.format(
                report_assessment.start_time,
                report_assessment.end_time,
                report_assessment.status,
                report_assessment.min_assessment_time,
                report_assessment.user_last_viewed,
                id,
                report_assessment.report_id,
                transformed_interaction_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_assessment_id = cursor.fetchone()
            return dict(report_assessment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, report_id: int, interaction_id: str):
    transformed_interaction_id = get_uuid(interaction_id)
    query = '''
                DELETE FROM report_assessments 
                WHERE id = %s
                AND report_id = %s
                AND interaction_id = %s
            '''
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (id, report_id, transformed_interaction_id))
            return {'message': f'Report assessment {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
