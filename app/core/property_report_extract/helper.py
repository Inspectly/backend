import os
import fitz
import json
import base64
import shutil
import requests
from io import BytesIO
from pathlib import Path
from typing import Union
from dotenv import load_dotenv

load_dotenv()

from app.core.property_report_extract.types import Issue
from app.core.property_report_extract.constants import MIN_IMAGE_SIZE, SCREENSHOT_ZOOM, DATA_OUTPUT_FOLDER

def write_issues_to_json(issues: list[Issue], filepath: Union[str, Path]):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents = True, exist_ok = True)
    issues_data = [issue.model_dump() for issue in issues]
    
    with open(filepath, 'w', encoding = 'utf-8') as f:
        json.dump(issues_data, f, ensure_ascii = False, indent = 2)

def extract_images_from_pdf(pdf_file, output_folder, logfire):
    try:
        total_image_count = 0
        extracted_images = []
        Path(output_folder).mkdir(parents = True, exist_ok = True)
        
        if isinstance(pdf_file, bytes):
            pdf_document = fitz.open(stream = pdf_file, filetype = 'pdf')
        elif isinstance(pdf_file, BytesIO):
            pdf_document = fitz.open(stream = pdf_file.read(), filetype = 'pdf')
        else:
            pdf_document = fitz.open(stream = pdf_file, filetype = 'pdf')
        
        for page_number in range(len(pdf_document)):
            images = pdf_document[page_number].get_images()
            for image_index_on_page, image in enumerate(images):
                total_image_count += 1
                pix = fitz.Pixmap(pdf_document, image[0])

                if (pix.n - pix.alpha >= 4):
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                image_bytes = pix.pil_tobytes(format = 'PNG')
                image_size = len(image_bytes)
                if (image_size < MIN_IMAGE_SIZE):
                    pix = None
                    continue

                filename = f'page_{page_number + 1:03d}_image_{image_index_on_page + 1:02d}_overall_{total_image_count:03d}.png'
                filepath = os.path.join(output_folder, filename)
                pix.save(filepath)
                extracted_images.append({
                    'page_number': page_number + 1,
                    'image_index_on_page': image_index_on_page + 1,
                    'overall_index': total_image_count,
                    'filepath': filepath,
                    'filename': filename
                })
                pix = None
        pdf_document.close()
        return extracted_images
    except Exception as e:
        logfire.error(f'Error in {extract_images_from_pdf.__name__}: {e}')
        raise ValueError(f'Error in {extract_images_from_pdf.__name__}: {e}') from e

def screenshot_pdf_pages(pdf_file, output_folder, logfire, zoom = SCREENSHOT_ZOOM):
    try:
        screenshots = []
        Path(output_folder).mkdir(parents = True, exist_ok = True)
        
        if isinstance(pdf_file, bytes):
            pdf_document = fitz.open(stream = pdf_file, filetype = 'pdf')
        elif isinstance(pdf_file, BytesIO):
            pdf_document = fitz.open(stream = pdf_file.read(), filetype = 'pdf')
        else:
            pdf_document = fitz.open(stream = pdf_file, filetype = 'pdf')
        
        matrix = fitz.Matrix(zoom, zoom)
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pix = page.get_pixmap(matrix = matrix)
            filename = f'page_{page_number + 1:03d}_screenshot.png'
            filepath = os.path.join(output_folder, filename)
            pix.save(filepath)
            screenshots.append({
                'page_number': page_number + 1,
                'filepath': filepath,
                'filename': filename
            })
            pix = None
        pdf_document.close()
        return screenshots
    except Exception as e:
        logfire.error(f'Error in {screenshot_pdf_pages.__name__}: {e}')
        raise ValueError(f'Error in {screenshot_pdf_pages.__name__}: {e}') from e

def upload_image_to_imgbb(image_file_path: str, logfire) -> str:
    with open(image_file_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    response = requests.post(
        os.getenv('IMGBB_API_URL'),
        {
            'key': os.getenv('IMGBB_API_KEY'),
            'image': image_data
        }
    )
    if response.status_code == 200:
        logfire.info(f'Image Successfully Uploaded: {response.json()["data"]["image"]["url"]}')
        return response.json()['data']['image']['url']
    else:
        logfire.error(f'ERROR: Server Response {response.status_code}: {response.json()["error"]["message"]}')
        return None

async def delete_images_and_screenshots(task_id: str) -> None:
    try:
        image_screenshots_folder = os.path.join(DATA_OUTPUT_FOLDER, str(task_id))
        shutil.rmtree(image_screenshots_folder)
    except Exception as e:
        raise ValueError(f'Error in {delete_images_and_screenshots.__name__}: {e}') from e
