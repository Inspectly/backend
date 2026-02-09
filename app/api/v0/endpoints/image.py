from fastapi import APIRouter, UploadFile, File

from app.crud import images

router = APIRouter()

@router.post('/')
async def upload(image: UploadFile = File(...)):
    return await images.upload_image(image)

@router.get('/{image_id}')
def get(image_id: str):
    return images.get_image(image_id)

@router.delete('/{image_id}')
def delete(image_id: str):
    return images.delete_image(image_id)
