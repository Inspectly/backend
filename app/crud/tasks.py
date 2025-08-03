from fastapi import HTTPException

from app.schema.tasks import Tasks
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM report_extraction_tasks 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code = 404, detail = 'Report extraction task not found')
        return dict(task)
    
def get_all():
    query = '''
                SELECT * 
                FROM report_extraction_tasks
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        tasks = cursor.fetchall()
        return [dict(task) for task in tasks]
    
def get_report_tasks(report_id: int):
    query = '''
                SELECT * 
                FROM report_extraction_tasks 
                WHERE report_id = {}
            '''.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        tasks = cursor.fetchall()
        return [dict(task) for task in tasks]
    
async def create(task: Tasks):
    query = '''
                INSERT INTO report_extraction_tasks 
                (report_id, task_type, status)
                VALUES ({}, '{}', '{}')
                RETURNING id
            '''.format(task.report_id, task.task_type, task.status)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        task_id = cursor.fetchone()
        return dict(task_id)
    
def update(id: int, task: Tasks):
    query = '''
                UPDATE report_extraction_tasks 
                SET status = '{}' 
                WHERE id = {} 
                AND report_id = {}
            '''.format(task.status, id, task.report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return True
