from fastapi import APIRouter, HTTPException, File, UploadFile

from app.crud import reports
from app.schema.properties import Reports
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
def create(report: Reports):
    return reports.create(report)

@router.post('/extract-issues') #add aws
def extract_issues(property_report: UploadFile = File(...)):
    if not property_report.filename.endswith('.pdf'):
        raise HTTPException(status_code = 400, detail = 'Only PDF files are allowed')
    extract_issues = Extract_Issues()
    return extract_issues.extract_issues(property_report, property_report.filename)


@router.put('/{id}')
def update(id: int, report: Reports):
    return reports.update(id, report)

@router.delete('/{id}')
def delete(id: int):
    return reports.delete(id)
