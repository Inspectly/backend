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
    IMAGE_DESCRIPTION_SYSTEM_PROMPT,
    IMAGE_CLASSIFIER_SYSTEM_PROMPT,
    IMAGE_EXTRACTOR_SYSTEM_PROMPT,
    IMAGE_VERIFIER_SYSTEM_PROMPT
)


class Agents:
    def __init__(self, **kwargs: Any):
        self.model_provider = ModelProvider(**kwargs)

        self.image_description_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = IMAGE_DESCRIPTION_SYSTEM_PROMPT,
            output_type = str,
        )

        self.image_classifier_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = IMAGE_CLASSIFIER_SYSTEM_PROMPT,
            output_type = ImageClassification,
        )

        self.image_extractor_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = IMAGE_EXTRACTOR_SYSTEM_PROMPT,
            output_type = Issue,
        )

        self.image_verifier_agent = Agent(
            self.model_provider.get_model(**kwargs),
            model_settings = self.model_provider.get_model_settings(**kwargs),
            system_prompt = IMAGE_VERIFIER_SYSTEM_PROMPT,
            output_type = Issue,
        )
