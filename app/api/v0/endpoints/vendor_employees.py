from fastapi import APIRouter

from app.crud import vendor_employees
from app.schema.users import Vendor_Employees

router = APIRouter()

@router.get('/vendor_id/{vendor_id}')
def get_all_by_vendor_id(vendor_id: int):
    return vendor_employees.get_all_by_vendor_id(vendor_id)

@router.get('/{id}')
def get_one(id: int):
    return vendor_employees.get_one(id)

@router.post('/')
def create(vendor_employee: Vendor_Employees):
    return vendor_employees.create(vendor_employee)

@router.put('/{id}')
def update(id: int, vendor_employee: Vendor_Employees):
    return vendor_employees.update(id, vendor_employee)

@router.delete('/{id}/{vendor_id}')
def delete(id: int, vendor_id: int):
    return vendor_employees.delete(id, vendor_id)
