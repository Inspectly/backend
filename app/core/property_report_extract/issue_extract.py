from typing import Any

from app.crud import tasks, issues
from app.schema.types import Status
from app.schema.properties import Issues
from app.core.property_report_extract.types import Issue
from app.core.property_report_extract.extract_image import ExtractImage
from app.core.property_report_extract.extract_issue import ExtractIssues
from app.core.property_report_extract.helper import write_issues_to_json
from app.core.common.llm_observability.pydantic_logfire.instrument_logfire import Instrument_Type, instrument_logfire
from app.schema.tasks import Tasks, Task_Type, Status as Task_Status

@instrument_logfire(instrument_type = Instrument_Type.PANDANTIC_AI, project = 'issue_extract')
class IssueExtract:
    def __init__(self, report_id: int, report_name: str, property_report: bytes, task_id: int):
        self.report_id = report_id
        self.report_name = report_name
        self.pdf = property_report
        self.task_id = task_id
        self.extract_issues = ExtractIssues(self)
        self.extract_images = ExtractImage(self)

    async def _extract_issues(self):
        issues = await self.extract_issues.extract_issues()
        self.logfire.info(f'Extracted {len(issues)} issues')
        return issues

    async def _extract_images(self, issues: list[Issue]):
        issues = await self.extract_images.extract_images(issues)
        self.logfire.info(f'Extracted {len(issues)} images')
        return issues

    async def run(self):
        with self.logfire.span(f'Extract Issues | {self.report_id}'):
            extracted_issues = await self._extract_issues()
            extracted_issues = await self._extract_images(extracted_issues)
            self.logfire.info(f'Extracted {len(extracted_issues)} issues. Extraction complete')
            self.logfire.info(f'Issues: {extracted_issues}')
            for issue in extracted_issues:
                new_issue = Issues(
                    report_id = self.report_id,
                    type = issue.type,
                    description = issue.description.replace("'", "''"),
                    summary = issue.name.replace("'", "''"),
                    status = Status.OPEN.value,
                    active = True,
                    image_urls = []
                )
                await issues.create(new_issue)
            self.logfire.info(f'Wrote {len(extracted_issues)} issues to database')
        await tasks.update(self.task_id, Tasks(
            id = self.task_id,
            report_id = self.report_id,
            task_type = Task_Type.EXTRACT_ISSUES.value,
            status = Task_Status.COMPLETED.value
        ))
