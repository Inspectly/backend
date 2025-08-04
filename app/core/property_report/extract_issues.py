import asyncio
import os
import json
from fastapi import UploadFile
from openai import OpenAI, AsyncOpenAI

from app.crud import tasks, issues
from app.schema.types import Status
from app.schema.properties import Issues
from app.core.property_report.prompt import PROMPT
from app.core.property_report.classes import Report_Response
from app.core.property_report.tools import REPORT_RESPONSE_TOOL
from app.core.property_report.report_parser import Report_Parser
from app.schema.tasks import Tasks, Task_Type, Status as Task_Status

class Extract_Issues:
    def __init__(self):
        self.parser = Report_Parser()
        self.llm = AsyncOpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )
    
    async def extract_issues(self, file_content: bytes, report_name: str, report_id: int, task_id: int):
        combined_content = self.parser.extract_combined_content(file_content, report_name)
        cc_json = json.dumps(combined_content, indent = 2, ensure_ascii = False)
        response = await self.llm.chat.completions.create(
            temperature = 0.2,
            model = 'gpt-4.1',
            messages = [
                {'role': 'system', 'content': 'You are an expert in home inspections.'},
                {'role': 'user', 'content': PROMPT.format(cc_json)}
            ],
            tools = [REPORT_RESPONSE_TOOL],
            tool_choice = {'type': 'function', 'function': {'name': 'generate_report_response'}}
        )
        try:
            arguments_str = response.choices[0].message.tool_calls[0].function.arguments
            structured_data = Report_Response.model_validate_json(arguments_str)

            print('✅ Successfully parsed structured report.')
            for issue_type in structured_data.IssueTypes:
                for issue in issue_type.issues:
                    new_issue = Issues(
                        report_id = report_id,
                        type = issue_type.type,
                        description = issue.description.replace("'", "''"),
                        summary = issue.name.replace("'", "''"),
                        status = Status.OPEN.value,
                        active = True,
                        image_url = ''
                    )
                    await issues.create(new_issue)
            print('✅ Successfully created issues.')
            await tasks.update(task_id, Tasks(
                id = task_id,
                report_id = report_id,
                task_type = Task_Type.EXTRACT_ISSUES.value,
                status = Task_Status.COMPLETED.value
            ))
        except Exception as e:
            print('Error: ', e)
            return None

if __name__ == '__main__':
    extract_issues = Extract_Issues()
    with open('1.pdf', 'rb') as file:
        file_content = file.read()

    result = asyncio.run(extract_issues.extract_issues(file_content, '1.pdf'))
    print(result)
