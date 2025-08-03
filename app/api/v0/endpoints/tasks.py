from fastapi import APIRouter

from app.crud import tasks
from app.schema.tasks import Tasks

router = APIRouter()

@router.get('/')
def get_all():
    return tasks.get_all()

@router.get('/{id}')
def get_one(id: int):
    return tasks.get_one(id)

@router.get('/report/{report_id}')
def get_report_tasks(report_id: int):
    return tasks.get_report_tasks(report_id)

@router.post('/')
def create(task: Tasks):
    return tasks.create(task)

@router.put('/{id}')
def update(id: int, task: Tasks):
    return tasks.update(id, task)
