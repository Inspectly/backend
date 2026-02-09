import os
import base64
import requests
from fastapi import UploadFile, File, HTTPException

IMGBB_API_URL = os.getenv('IMGBB_API_URL')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')

async def upload_image(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image_data = base64.b64encode(image_bytes).decode('utf-8')
    response = requests.post(
        IMGBB_API_URL,
        {
            'key': IMGBB_API_KEY,
            'image': image_data
        }
    )
    if response.status_code == 200:
        return response.json()['data']
    raise HTTPException(status_code = response.status_code, detail = response.json().get('error', {}).get('message', 'Upload failed'))

def get_image(image_id: str):
    response = requests.get(f'{IMGBB_API_URL}/{image_id}', params = {'key': IMGBB_API_KEY})
    if response.status_code == 200:
        return response.json()['data']
    raise HTTPException(status_code = response.status_code, detail = response.json().get('error', {}).get('message', 'Image not found'))

def delete_image(image_id: str):
    response = requests.delete(f'{IMGBB_API_URL}/{image_id}', params = {'key': IMGBB_API_KEY})
    if response.status_code == 200:
        return {'message': f'Image {image_id} deleted successfully'}
    raise HTTPException(status_code = response.status_code, detail = response.json().get('error', {}).get('message', 'Delete failed'))
