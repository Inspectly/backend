from fastapi import APIRouter, HTTPException, Body

from app.crud import report_offers
from app.schema.properties import Report_Offers

router = APIRouter()

@router.get('/')
def get_all():
    return report_offers.get_all()

@router.get('/{id}')
def get_one(id: int):
    return report_offers.get_one(id)

@router.get('/report/{report_id}')
def get_all_by_report_id(report_id: int):
    return report_offers.get_all_by_report_id(report_id)

@router.get('/vendor/{vendor_id}')
def get_all_by_vendor_id(vendor_id: int):
    return report_offers.get_all_by_vendor_id(vendor_id)

@router.get('/vendor/{vendor_id}/report/{report_id}')
def get_all_by_vendor_id(vendor_id: int, report_id: int):
    return report_offers.get_all_by_vendor_id_and_report_id(vendor_id, report_id)

@router.post('/')
def create(report_offer: Report_Offers):
    return report_offers.create(report_offer)

@router.put('/{id}')
def update(id: int, report_offer: Report_Offers):
    return report_offers.update(id, report_offer)

@router.delete('/{id}')
def delete(id: int, report_id: int = Body(..., embed = True)):
    return report_offers.delete(id, report_id)
