import logging
import os
from abc import abstractmethod
from typing import Generic, TypeVar

import tenacity
from pydantic import BaseModel, ConfigDict, PrivateAttr

from opengates.ai_gateway.policy.guardrails import BaseGuardrail
from opengates.ai_gateway.policy.guardrails.base import GuardrailAction
from opengates.messages import BaseMessage, UserMessage

__all__ = [
    "BaseCompletion",
]

MULTIPLIER = 1
MIN_WAIT = 1
MAX_WAIT = 60
STOP_AFTER_ATTEMPT = 10

logger = logging.getLogger(__name__)
ClientT = TypeVar("ClientT")


class BaseCompletion(BaseModel, Generic[ClientT]):
    model_config = ConfigDict(extra="forbid")
    api_key: str
    model_name: str

    _client: ClientT | None = PrivateAttr(default=None)

    def __init__(
        self,
        api_key_env_var: str,
        model_name: str,
    ):
        api_key = os.getenv(api_key_env_var)
        if not api_key:
            raise ValueError(
                f"API key not found in environment variable: {api_key_env_var}"
            )

        super().__init__(
            api_key=api_key,
            model_name=model_name,
        )

    @property
    def client(self) -> ClientT:
        if self._client is None:
            self._client = self._initialize_client()
        return self._client

    @abstractmethod
    def _initialize_client(self) -> ClientT:
        raise NotImplementedError

    @tenacity.retry(
        wait=tenacity.wait_exponential(
            multiplier=MULTIPLIER, min=MIN_WAIT, max=MAX_WAIT
        ),
        stop=tenacity.stop_after_attempt(max_attempt_number=STOP_AFTER_ATTEMPT),
        retry=tenacity.retry_if_exception_type((TimeoutError, ConnectionError)),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def generate(
        self,
        history: list[BaseMessage],
    ) -> str:
        history_raw = self._history_to_raw(history)
        response = self._generate_logic(history_raw)
        return response

    def _apply_guardrails(
        self,
        guardrails: list[BaseGuardrail],
        text: str,
    ) -> None:
        for guardrail in guardrails:
            guardrail_result = guardrail.apply(text)
            if guardrail_result == GuardrailAction.BLOCK:
                raise ValueError("Content contains forbidden content")
            elif guardrail_result == GuardrailAction.WARN:
                logger.warning(
                    f"Guardrail {guardrail.__class__.__name__} triggered: {text}"
                )

    @abstractmethod
    def _generate_logic(
        self,
        history_raw: list[dict],
    ) -> str:
        raise NotImplementedError

    def _format_history(
        self,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> list[BaseMessage]:
        if isinstance(history, str):
            return [UserMessage(content=history)]
        elif isinstance(history, BaseMessage):
            return [history]
        elif isinstance(history, list):
            return history
        else:
            raise ValueError("Invalid history format")

    def _history_to_raw(
        self,
        history: list[BaseMessage],
    ) -> list[dict]:
        return [
            msg.model_dump_json(exclude_none=True, serialize_as_any=True)
            for msg in history
        ]
