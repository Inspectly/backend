import os
from typing import Any
from openai import AsyncOpenAI
from pydantic_ai import models
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIResponsesModel, OpenAIResponsesModelSettings

from app.core.common.models.open_ai import OpenAIModels
from app.core.common.framework.pydantic.model_provider import IModelProvider

class ModelProvider(IModelProvider):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.primary_model = kwargs.get('primary_model', OpenAIModels.gpt_5_1)
        self.fallback_model = kwargs.get('fallback_model', OpenAIModels.gpt_4_1_mini)
        self.openai_provider = OpenAIProvider(openai_client = AsyncOpenAI(api_key = os.getenv('OPENAI_API_KEY')))
        

    def get_model(self, **kwargs: Any) -> models.Model:
        print(f'Getting model: {self.primary_model.model_name}')
        return FallbackModel(
            OpenAIResponsesModel(
                model_name = self.primary_model.model_name,
                provider = self.openai_provider,
            ),
            OpenAIResponsesModel(
                model_name = self.fallback_model.model_name,
                provider = self.openai_provider,
            )
        )
    
    def get_model_settings(self, **kwargs: Any) -> OpenAIResponsesModelSettings:
        if (kwargs.get('high_effort')):
            if (self.primary_model.model_settings.allow_temperature):
                return OpenAIResponsesModelSettings(
                    temperature = 0.0,
                    reasoning_effort = 'high',
                )
            else:
                return OpenAIResponsesModelSettings(
                    reasoning_effort = 'high',
                )
        return None
