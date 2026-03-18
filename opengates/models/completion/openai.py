from typing import Any, Literal

from openai import OpenAI

from opengates.models.completion.base import BaseCompletion
from opengates.models.completion.result import CompletionResult

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
    ) -> None:
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
        history_raw: list[dict[str, Any]],
    ) -> dict[str, Any]:
        response = self.client.responses.create(
            model=self.model_name,
            input=history_raw,
        )
        return response

    def _parse_response(
        self,
        response_raw: dict[str, Any],
    ) -> CompletionResult:
        text = response_raw.text  # type: ignore
        usage = getattr(response_raw, "usage", None)

        input_tokens = (
            getattr(usage, "input_tokens", None)
            or getattr(usage, "prompt_tokens", 0)
            or 0
        )
        output_tokens = (
            getattr(usage, "output_tokens", None)
            or getattr(usage, "completion_tokens", 0)
            or 0
        )

        return CompletionResult(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
