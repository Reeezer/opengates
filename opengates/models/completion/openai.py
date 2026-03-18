from typing import Literal

from openai import OpenAI

from opengates.models.completion.base import BaseCompletion

__all__ = [
    "OpenAICompletion",
]

# https://developers.openai.com/api/docs/models/

MODELS = Literal[
    "gpt-5.4-2026-03-05",
    "gpt-5.4-pro-2026-03-05",
    "gpt-5-mini-2025-08-07",
    "gpt-5-nano-2025-08-07",
    "gpt-5-2025-08-07",
    "gpt-4.1-2025-04-14",
]


class OpenAICompletion(BaseCompletion[OpenAI]):
    def __init__(
        self,
        api_key_env_var: str = "OPENAI_API_KEY",
        model_name: MODELS = "gpt-5-mini-2025-08-07",
    ):
        super().__init__(
            api_key_env_var=api_key_env_var,
            model_name=model_name,
        )

    def _initialize_client(
        self,
    ) -> OpenAI:
        return OpenAI(api_key=self.api_key)

    def _generate_logic(
        self,
        history_raw: list[dict],
    ) -> str:
        response = self.client.responses.create(
            model=self.model_name,
            input=history_raw,
        )
        return response.text
