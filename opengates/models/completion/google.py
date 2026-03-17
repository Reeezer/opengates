from typing import Literal

from google import genai

from opengates.messages.base import BaseMessage
from opengates.models.completion.base import BaseCompletion

__all__ = [
    "GoogleCompletion",
]

# https://ai.google.dev/gemini-api/docs/models

MODELS = Literal[
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
]


class GoogleCompletion(BaseCompletion):
    client: genai.Client

    def __init__(
        self,
        api_key_env_var: str = "GOOGLE_API_KEY",
        model_name: MODELS = "gemini-2.5-flash-lite",
    ):
        super().__init__(api_key_env_var=api_key_env_var, model_name=model_name)
        self.client = genai.Client(api_key=self.api_key)

    def _generate_logic(
        self,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self._format_history(history),
        )
        return response.text
