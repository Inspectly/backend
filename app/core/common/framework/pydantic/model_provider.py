from typing import Protocol, Any
from pydantic_ai import models
from pydantic_ai.settings import ModelSettings

class IModelProvider(Protocol):
    def get_model(self, **kwargs: Any) -> models.Model: ...
    def get_model_settings(self, **kwargs: Any) -> ModelSettings: ...
