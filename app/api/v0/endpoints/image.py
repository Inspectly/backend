from fastapi import APIRouter, UploadFile, File

from app.crud import images

router = APIRouter()

@router.post('/')
async def upload(image: UploadFile = File(...)):
    return await images.upload_image(image)
