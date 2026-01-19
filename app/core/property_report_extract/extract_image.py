import os
import asyncio
from typing import List
from pathlib import Path
from pydantic_ai.messages import BinaryContent

from app.core.property_report_extract.types import Issue
from app.core.common.models.open_ai import OpenAIModels
from app.core.property_report_extract.agents.agents_image import Agents
from app.core.property_report_extract.constants import DATA_OUTPUT_FOLDER
from app.core.property_report_extract.helper import extract_images_from_pdf, screenshot_pdf_pages, delete_images_and_screenshots, upload_image_to_imgbb
from app.core.property_report_extract.prompts.prompts import (
    IMAGE_DESCRIPTION_USER_PROMPT,
    IMAGE_CLASSIFIER_USER_PROMPT,
    IMAGE_EXTRACTOR_USER_PROMPT,
    IMAGE_VERIFIER_USER_PROMPT
)

class ExtractImage:
    def __init__(self, parent):
        self.parent = parent
        self.pdf = parent.pdf
        self.report_id = parent.report_id
        self.logfire = parent.logfire
        self.agents = Agents(
            primary_model = OpenAIModels.gpt_5_mini,
            high_effort = True
        )
        self.task_id = parent.task_id

    async def _extract_images_screenshots_metadata(self):
        images = extract_images_from_pdf(self.pdf, os.path.join(DATA_OUTPUT_FOLDER, str(self.task_id), 'images'), self.logfire)
        screenshots = screenshot_pdf_pages(self.pdf, os.path.join(DATA_OUTPUT_FOLDER, str(self.task_id), 'screenshots'), self.logfire)
        return images, screenshots

    async def _get_image_description(self, image_data):
        image_description = await self.agents.image_description_agent.run(
            [
                BinaryContent(
                    data = image_data, 
                    media_type = 'image/png'
                ),
                IMAGE_DESCRIPTION_USER_PROMPT
            ]
        )
        return image_description.output
    
    async def _get_image_classification(self, image_data, description):
        image_classification = await self.agents.image_classifier_agent.run(
            [
                BinaryContent(
                    data = image_data, 
                    media_type = 'image/png'
                ),
                IMAGE_CLASSIFIER_USER_PROMPT.format(
                    description = description
                )
            ]
        )
        return image_classification.output.is_issue

    async def _process_single_image(self, image):
        image_data = Path(image['filepath']).read_bytes()
        description = await self._get_image_description(image_data)
        image['description'] = description
        classification = await self._get_image_classification(image_data, description)
        image['is_issue'] = classification
        if classification:
            image['imgbb_url'] = upload_image_to_imgbb(image['filepath'], self.logfire)
        return image

    async def _assign_image_to_issue(self, image: dict, screenshot_data: bytes, issues: List[Issue]) -> dict:
        image_data = Path(image['filepath']).read_bytes()
        
        response = await self.agents.image_extractor_agent.run(
            user_prompt = [
                BinaryContent(data = screenshot_data, media_type = 'image/png'),
                BinaryContent(data = image_data, media_type = 'image/png'),
                IMAGE_EXTRACTOR_USER_PROMPT.format(
                    image_name = image['filename'],
                    image_description = image['description'],
                    issues = issues
                )
            ]
        )
        return {'filename': image['filename'], 'issue_id': response.output.id, 'imgbb_url': image['imgbb_url']}

    async def _verify_single_issue(self, issue: Issue, issue_images_dict: dict, screenshots_dict: dict) -> Issue:
        if not issue.images:
            return issue
        
        image_details = []
        for idx, image_filename in enumerate(issue.images, start = 1):
            if image_filename in issue_images_dict:
                image_meta = issue_images_dict[image_filename]
                image_details.append(f"{idx}. {image_filename}\n   Description: {image_meta['description']}")
        
        user_prompt_parts = [
            IMAGE_VERIFIER_USER_PROMPT.format(
                issue_id = issue.id,
                issue_name = issue.name,
                issue_description = issue.description,
                issue_type = issue.type.value if issue.type else '',
                image_count = len(issue.images),
                image_details = '\n'.join(image_details)
            )
        ]
        
        for image_filename in issue.images:
            if image_filename in issue_images_dict:
                image_meta = issue_images_dict[image_filename]
                
                screenshot_data = Path(screenshots_dict[image_meta['page_number']]).read_bytes()
                user_prompt_parts.append(BinaryContent(data = screenshot_data, media_type = 'image/png'))
                
                image_data = Path(image_meta['filepath']).read_bytes()
                user_prompt_parts.append(BinaryContent(data = image_data, media_type = 'image/png'))
        
        response = await self.agents.image_verifier_agent.run(user_prompt = user_prompt_parts)
        return response.output
    
    async def extract_images(self, issues: List[Issue]):
        try:
            images, screenshots = await self._extract_images_screenshots_metadata()
            screenshots_dict = {s['page_number']: s['filepath'] for s in screenshots}
            self.logfire.info(f'Extracted {len(images)} images and {len(screenshots)} screenshots')

            processed_images = await asyncio.gather(
                *[self._process_single_image(image) for image in images]
            )
            self.logfire.info(f'Processed {len(processed_images)} images | Number of issue images = {sum(1 for image in processed_images if image["is_issue"])}')
            
            if (sum(1 for image in processed_images if image['is_issue']) == 0):
                self.logfire.info('No issue images found')
                return issues
            
            issue_images = []
            for image in processed_images:
                if image['is_issue']:
                    issue_images.append(image)
            

            for idx, issue in enumerate(issues, start = 1):
                issue.id = idx

            assignments = await asyncio.gather(*[
                self._assign_image_to_issue(
                    image, 
                    Path(screenshots_dict[image['page_number']]).read_bytes(), 
                    issues
                ) 
                for image in issue_images
            ])
            for assignment in assignments:
                for issue in issues:
                    if (issue.id == assignment['issue_id']):
                        issue.images.append(assignment['filename'])
                        break
                        
            self.logfire.info(f'Assigned {len(assignments)} images to issues')
            
            
            issue_images_dict = {img['filename']: img for img in issue_images}
        
            verified_issues = await asyncio.gather(*[
                self._verify_single_issue(issue, issue_images_dict, screenshots_dict)
                for issue in issues
            ])

            for issue in verified_issues:
                for image_filename in issue.images:
                    for assignment in assignments:
                        if assignment['filename'] == image_filename:
                            issue.imgbb_urls.append(assignment['imgbb_url'])
                            break

            return verified_issues

        except Exception as e:
            self.logfire.error(f'Error extracting issues: {e}')
            raise e
        
        finally:
            try:
                await delete_images_and_screenshots(self.task_id)
                self.logfire.info(f'Deleted images and screenshots for task {self.task_id}')
            except Exception as e:
                self.logfire.error(f'Error deleting images and screenshots: {e}')
