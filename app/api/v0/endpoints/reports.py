import json
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, BackgroundTasks

from app.crud import reports, tasks
from app.schema.tasks import Tasks, Task_Type, Status
from app.schema.properties import Reports, Reports_Simple
from app.core.property_report.aws_operations import AWS_Operations
from app.core.property_report.extract_issues import Extract_Issues

router = APIRouter()

@router.get('/')
def get_all():
    return reports.get_all()

@router.get('/{id}')
def get_one(id: int):
    return reports.get_one(id)

@router.get('/user/{user_id}')
def get_user_reports(user_id: int):
    return reports.get_user_reports(user_id)

@router.get('/listing/{listing_id}')
def get_listing_reports(listing_id: int):
    return reports.get_listing_reports(listing_id)

@router.post('/')
async def create(report: Reports):
    return await reports.create(report)

@router.post('/extract/issues')
async def extract_issues(
    background_tasks: BackgroundTasks,
    user_id: int = Form(...),
    listing_id: int = Form(...), 
    name: str = Form(...),
    property_report: UploadFile = File(...)
):
    if not property_report.filename.endswith('.pdf'):
        raise HTTPException(status_code = 400, detail = 'Only PDF files are allowed')
    
    file_content = await property_report.read()
    await property_report.seek(0)

    # aws_operations = AWS_Operations()
    # aws_link = await aws_operations.upload_file(user_id, listing_id, name, property_report)
    aws_link = 'temp:link:aws:s3'
    report = await reports.create(Reports(
        user_id = user_id,
        listing_id = listing_id,
        aws_link = aws_link,
        name = name
    ))
    task_id = await tasks.create(Tasks(
        report_id = report['id'], 
        task_type = Task_Type.EXTRACT_ISSUES.value, 
        status = Status.PENDING.value
    ))
    extract_issues = Extract_Issues()
    background_tasks.add_task(extract_issues.extract_issues, file_content, property_report.filename, report['id'], task_id['id'])
    return {
        'report_id': report['id'], 
        'task_id': task_id['id'], 
        'aws_link': aws_link
    }


@router.put('/{id}')
def update(id: int, report: Reports):
    return reports.update(id, report)

@router.delete('/{id}')
def delete(id: int):
    return reports.delete(id)
