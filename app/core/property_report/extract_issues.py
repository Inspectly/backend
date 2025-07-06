import os
import json
from fastapi import UploadFile
from openai import OpenAI, AsyncOpenAI

from app.core.property_report.prompt import PROMPT
from app.core.property_report.classes import Report_Response
from app.core.property_report.tools import REPORT_RESPONSE_TOOL
from app.core.property_report.report_parser import Report_Parser


class Extract_Issues:
    def __init__(self):
        self.parser = Report_Parser()
        self.llm = OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )
    
    def extract_issues(self, file_content: bytes, report_name: str):
        combined_content = self.parser.extract_combined_content(file_content, report_name)
        cc_json = json.dumps(combined_content, indent = 2, ensure_ascii = False)
        response = self.llm.chat.completions.create(
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

            print("✅ Successfully parsed structured report.")
            return structured_data
        except Exception as e:
            print('Error: ', e)
            return None

if __name__ == '__main__':
    extract_issues = Extract_Issues()
    print(extract_issues.extract_issues('1.pdf', '1.pdf'))
