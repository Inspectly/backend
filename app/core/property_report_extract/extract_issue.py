import asyncio
from pydantic_ai.messages import BinaryContent

from app.core.common.models.open_ai import OpenAIModels
from app.core.property_report_extract.types import IssueTypes
from app.core.property_report_extract.agents.agents_issue import Agents
from app.core.property_report_extract.prompts.prompts import (
    ISSUES_EXTRACT_USER_PROMPT,
    ISSUES_VERIFIER_USER_PROMPT,
    ISSUE_VALIDATION_USER_PROMPT,
    ISSUE_TYPE_USER_PROMPT,
    ISSUE_TYPE_VALIDATION_USER_PROMPT
)

class ExtractIssues:
    def __init__(self, parent):
        self.parent = parent
        self.pdf = parent.pdf
        self.report_id = parent.report_id
        self.logfire = parent.logfire
        self.agents = Agents(
            primary_model = OpenAIModels.gpt_5_mini,
            high_effort = True
        )

    async def extract_issues(self):
        try:
            extracted_issues = await self.agents.issues_extract_agent.run([
                ISSUES_EXTRACT_USER_PROMPT,
                BinaryContent(data = self.pdf, media_type = 'application/pdf')
            ])
            self.logfire.info(f'Extracted {len(extracted_issues.output.issues)} issue types')
            self.logfire.info(f'Extracted issues: {extracted_issues.output.issues}')

            extracted_issues_verified = await self.agents.issues_verifier_agent.run([
                ISSUES_VERIFIER_USER_PROMPT.format(issues = extracted_issues.output.issues),
                BinaryContent(data = self.pdf, media_type = 'application/pdf')
            ])
            self.logfire.info(f'Verified {len(extracted_issues_verified.output.issues)} issue types')
            self.logfire.info(f'Verified issues: {extracted_issues_verified.output.issues}')

            issue_validation_tasks = [
                self.agents.issue_validator_agent.run([
                    ISSUE_VALIDATION_USER_PROMPT.format(issue = issue),
                    BinaryContent(data = self.pdf, media_type = 'application/pdf')
                ])
                for issue in extracted_issues_verified.output.issues
            ]
            validated_issues_task = await asyncio.gather(*issue_validation_tasks)
            validated_issues = [result.output for result in validated_issues_task]
            self.logfire.info(f'Validated {len(validated_issues)} issues')

            issue_type_tasks = [
                self.agents.issue_type_agent.run([
                    ISSUE_TYPE_USER_PROMPT.format(
                        issue_name = validated_issue.name,
                        issue_description = validated_issue.description
                    ),
                    BinaryContent(data = self.pdf, media_type = 'application/pdf')
                ])
                for validated_issue in validated_issues
            ]
            issue_types = await asyncio.gather(*issue_type_tasks)
            self.logfire.info(f'Generated types for {len(issue_types)} issues')
            for validated_issue, issue_type_result in zip(validated_issues, issue_types):
                validated_issue.type = IssueTypes(issue_type_result.output.strip().upper())
                self.logfire.info(f'Assigned type {issue_type_result.output} to issue: {validated_issue.name}')

            issue_type_validation_tasks = [
                self.agents.issue_type_validator_agent.run([
                    ISSUE_TYPE_VALIDATION_USER_PROMPT.format(
                        issue_name = validated_issue.name,
                        issue_description = validated_issue.description,
                        assigned_issue_type = validated_issue.type
                    ),
                    BinaryContent(data = self.pdf, media_type = 'application/pdf')
                ])
                for validated_issue in validated_issues
            ]
            validated_issue_types = await asyncio.gather(*issue_type_validation_tasks)
            validated_issue_types = [result.output for result in validated_issue_types]
            self.logfire.info(f'Validated types for {len(validated_issue_types)} issues')
            for validated_issue, validated_type_result in zip(validated_issues, validated_issue_types):
                validated_issue.type = IssueTypes(validated_type_result.upper())
                self.logfire.info(f'Validated and assigned type {validated_type_result} to issue: {validated_issue.name}')

            self.logfire.info(f'Validated {len(validated_issues)} issues')
            self.logfire.info(f'Validated issues: {validated_issues}')
            return validated_issues

        except Exception as e:
            self.logfire.error(f'Error extracting issues: {e}')
            raise e
