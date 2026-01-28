from app.core.common.models.types import Provider, ReasoningEffort, Settings, Models, ReasoningEffort

class OpenAIModels:
    gpt_4_1_mini = Models(
        model_name = 'gpt-4.1-mini',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = True,
            allow_reasoning_effort = False,
            reasoning_effort = ReasoningEffort.low,
        )
    )

    gpt_5_1 = Models(
        model_name = 'gpt-5.1',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = False,
            allow_reasoning_effort = True,
            reasoning_effort = ReasoningEffort.low,
        )
    )

    gpt_5_mini = Models(
        model_name = 'gpt-5-mini',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = False,
            allow_reasoning_effort = True,
            reasoning_effort = ReasoningEffort.low,
        )
    )

    gpt_5 = Models(
        model_name = 'gpt-5',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = False,
            allow_reasoning_effort = True,
            reasoning_effort = ReasoningEffort.low,
        )
    )

    o4_mini = Models(
        model_name = 'o4-mini',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = True,
            allow_reasoning_effort = True,
            reasoning_effort = ReasoningEffort.low,
        )
    )

    o3_mini = Models(
        model_name = 'o3-mini',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = True,
            allow_reasoning_effort = True,
            reasoning_effort = ReasoningEffort.low,
        )
    )

    o3 = Models(
        model_name = 'o3',
        provider = Provider.openai,
        model_settings = Settings(
            allow_temperature = True,
            allow_reasoning_effort = True,
            reasoning_effort = ReasoningEffort.low,
        )
    )
