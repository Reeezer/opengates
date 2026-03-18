import logging
import os
from abc import abstractmethod
from typing import Any, Generic, TypeVar

import tenacity
from pydantic import BaseModel, ConfigDict, PrivateAttr

from opengates.messages import BaseMessage
from opengates.models.completion.result import CompletionResult

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
    ) -> None:
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
    ) -> CompletionResult:
        history_raw = self._history_to_raw(history)
        response_raw = self._generate_logic(history_raw)
        response = self._parse_response(response_raw)
        return response

    def _history_to_raw(
        self,
        history: list[BaseMessage],
    ) -> list[dict[str, Any]]:
        return [
            msg.model_dump_json(exclude_none=True, serialize_as_any=True)
            for msg in history
        ]

    @abstractmethod
    def _generate_logic(
        self,
        history_raw: list[dict[str, Any]],
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def _parse_response(
        self,
        response_raw: dict[str, Any],
    ) -> CompletionResult:
        raise NotImplementedError
