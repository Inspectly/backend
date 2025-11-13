from typing import Any

from pydantic_ai import Agent

from app.core.property_report_extract.model_provider import ModelProvider
from app.core.property_report_extract.types import (
    ReportIssues,
    IssueTypes,
    Issue,
    ImageClassification
)
from app.core.property_report_extract.prompts.prompts import (
    ISSUES_EXTRACT_SYSTEM_PROMPT,
    ISSUE_TYPE_VALIDATION_SYSTEM_PROMPT,
    ISSUES_VERIFIER_SYSTEM_PROMPT,
    ISSUE_VALIDATION_SYSTEM_PROMPT,
    ISSUE_TYPE_SYSTEM_PROMPT
)

class Agents:
    def __init__(self, **kwargs: Any):
        self.model_provider = ModelProvider(**kwargs)

        self.issues_extract_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = ISSUES_EXTRACT_SYSTEM_PROMPT,
            output_type = ReportIssues
        )

        self.issues_verifier_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = ISSUES_VERIFIER_SYSTEM_PROMPT,
            output_type = ReportIssues
        )

        self.issue_validator_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = ISSUE_VALIDATION_SYSTEM_PROMPT,
            output_type = Issue
        )

        self.issue_type_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = ISSUE_TYPE_SYSTEM_PROMPT,
            output_type = str
        )

        self.issue_type_validator_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = ISSUE_TYPE_VALIDATION_SYSTEM_PROMPT,
            output_type = str
        )
