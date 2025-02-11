from fastapi import HTTPException

from app.schema.properties import Notes
from app.core.database import get_db_cursor

def get_one(id: int):
    query = """
                SELECT * 
                FROM notes 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        note = cursor.fetchone()
        if not note:
            raise HTTPException(status_code = 404, detail = 'Note not found')
        return dict(note)

def get_all():
    query = """
                SELECT * 
                FROM notes 
                ORDER BY id DESC
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        notes = cursor.fetchall()
        return [dict(note) for note in notes]

def get_report_notes(report_id: int):
    query = """
                SELECT * 
                FROM notes 
                WHERE report_id = {}
            """.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        notes = cursor.fetchall()
        return [dict(note) for note in notes]

def get_user_notes(user_id: int):
    query = """
                SELECT * 
                FROM notes 
                WHERE user_id = {}
            """.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        notes = cursor.fetchall()
        return [dict(note) for note in notes]

def create(note: Notes):
    query = """
                INSERT INTO notes (report_id, user_id, note)
                VALUES ({}, {}, '{}')
                RETURNING id, report_id, user_id, note, created_at
            """.format(note.report_id, note.user_id, note.note)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        note = cursor.fetchone()
        return dict(note)

def update(id: int, note: Notes):
    query = """
                UPDATE notes 
                SET note = '{}'
                WHERE id = {}
                RETURNING id, report_id, user_id, note, updated_at
            """.format(note.note, id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        note = cursor.fetchone()
        return dict(note)

def delete(id: int):
    query = """
                DELETE FROM notes 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Note {id} deleted successfully'}
